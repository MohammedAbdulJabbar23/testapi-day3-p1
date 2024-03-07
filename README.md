# testapi-day3-p1# 

Registration Endpoint:

URL: POST /register

Description: Registers a new user.

Request Body:

    username (string, required): The email address of the user.
    password (string, required): The password for the user account.

Example:

json

{
    "username": "user",
    "password": "password123"
}

Login Endpoint:

URL: POST /token

Description: Logs in an existing user and generates a JWT token.

Request Body:

    username (string, required): The email address of the user.
    password (string, required): The password for the user account.

Example:

json

{
    "username": "user@example.com",
    "password": "password123"
}

WebSocket Connection:

URL: ws://your-server-hostname/ws

Description: Connects to the WebSocket endpoint for real-time communication.

Headers:

    Authorization (string, required): Bearer token received from the login endpoint.

Example:

http

GET /ws HTTP/1.1
Host: your-server-hostname

Authorization: Bearer eyJ0eXAiOiJKV1QiLCJhbGciOiJIUzI1NiJ9...

Ensure to replace your-server-hostname with your server's hostname or IP address.

This documentation provides clear guidelines on what JSON data to send for user registration and login, as well as how to authenticate WebSocket connections using the generated JWT token.
