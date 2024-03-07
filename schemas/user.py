from pydantic import BaseModel

class UserBase(BaseModel):
    username: str

class UserCreate(UserBase):
    username:str
    password: str

class UserInDB(UserBase):
    id: int
    class Config:
        orm_mode = True


class Token(BaseModel):
    access_token: str
    token_type: str

