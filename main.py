from fastapi import FastAPI, WebSocket, Depends, HTTPException, status
from models.models import Room, Message
from models.user import User
from socketio import AsyncServer
from datetime import datetime
from fastapi.middleware.cors import CORSMiddleware
from routes import user
from utils.auth import get_current_user
from tortoise import Tortoise
app = FastAPI()
sio = AsyncServer(async_mode='asgi')

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  
    allow_credentials=True,
    allow_methods=["*"],  
    allow_headers=["*"],  
)

@app.on_event("startup")
async def startup():
    await Tortoise.init(
        db_url='sqlite://db.sqlite3',
        modules={'models': ['models.models','models.user']},
    )
    await Tortoise.generate_schemas()

@app.on_event("shutdown")
async def shutdown():
    await Tortoise.close_connections()


# Store all connected users
clients = {}

@app.websocket("/ws/{room}")
async def websocket_endpoint(room: str, websocket: WebSocket, current_user: User = Depends(get_current_user)):
    await websocket.accept()
    clients[room] = clients.get(room, set())
    clients[room].add(websocket)

    try:
        while True:
            data = await websocket.receive_text()

            for client in clients[room]:
                await client.send_text(data)
            
            # Store message in the database
            room_obj, created = await Room.get_or_create(name=room)
            print(room_obj)

            if room_obj:  # Check if the room exists
                message = Message(room=room_obj, sender=current_user.username, content=data)
                await message.save()
    except Exception as e:
        print("WebSocket Error:", e)
    finally:
        # Remove the users when disconnected
        clients[room].remove(websocket)


@sio.on('connect')
async def connect(sid, environ):
    token = environ.get("HTTP_AUTHORIZATION")
    if not token:
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="Authorization header is missing")
    
    # Verify token and get current user
    current_user = await get_current_user(token)
    
    print(f"Client connected: {sid}")
    await sio.emit('message', 'Welcome to the server!', room=sid)

@sio.on('disconnect')
async def disconnect(sid):
    print(f"Client disconnected: {sid}")
    for room, room_clients in clients.items():
        if sid in room_clients:
            room_clients.remove(sid)

@app.get("/history/{room}")
async def get_chat_history(room: str, current_user: User = Depends(get_current_user)):
    messages = await Message.filter(room__name=room).order_by('timestamp').all()
    return [{"sender": message.sender, "message": message.content, "timestamp":message.timestamp} for message in messages]

app.include_router(user.router)

if __name__ == "__main__":
    import uvicorn
    from fastapi import BackgroundTasks

    uvicorn.run(app, host="0.0.0.0", port=8000)
