from pydantic import BaseModel
from tortoise import fields
from tortoise.models import Model

class User(Model):
    id = fields.IntField(pk=True)
    username = fields.CharField(max_length=50, unique=True)
    password_hash = fields.CharField(max_length=100)

    def __str__(self):
        return self.username

class Token(BaseModel):
    access_token: str
    token_type: str




