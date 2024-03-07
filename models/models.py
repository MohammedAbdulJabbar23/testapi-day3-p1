from tortoise import Tortoise, fields
from tortoise.models import Model



class Room(Model):
    id = fields.IntField(pk=True)
    name = fields.CharField(max_length=50)

class Message(Model):
    id = fields.IntField(pk=True)
    room = fields.ForeignKeyField("models.Room", related_name='messages')
    sender = fields.CharField(max_length=50)
    content = fields.TextField()
    timestamp = fields.DatetimeField(auto_now_add=True, null=True)
