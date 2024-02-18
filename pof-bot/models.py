from peewee import (
    Model,
    SqliteDatabase,
    IntegerField,
    CharField,
)

db = SqliteDatabase("bot.db")


def create_tables():
    with db:
        db.create_tables([User])

def drop_tables():
    with db:
        db.drop_tables([User])


class BaseModel(Model):
    class Meta:
        database = db


class User(BaseModel):
    user_id = IntegerField(unique=True)

    username = CharField(max_length=200, null=True)
    first_name = CharField(max_length=500)
    last_name = CharField(max_length=500, null=True)
