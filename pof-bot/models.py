import os
from peewee import Model, SqliteDatabase, IntegerField, CharField

# Define the database file name
DB_NAME = "bot.db"

# Initialize the SQLite database connection.
# SQLite will automatically create the database file if it does not exist.
db = SqliteDatabase(DB_NAME)


class BaseModel(Model):
    """
    Base model that sets the database for all inheriting models.
    """
    class Meta:
        database = db


class User(BaseModel):
    """
    User model for storing user information.
    """
    user_id = IntegerField(unique=True)
    username = CharField(max_length=200, null=True)
    first_name = CharField(max_length=500)
    last_name = CharField(max_length=500, null=True)


def create_tables() -> None:
    """
    Connect to the database and create the necessary tables.
    If the database file does not exist, it will be created automatically.
    """
    # Connect to the database (creates the database file if it doesn't exist)
    db.connect()
    # Create tables safely (won't throw an error if table already exists)
    db.create_tables([User], safe=True)
    db.close()


def drop_tables() -> None:
    """
    Connect to the database and drop the specified tables.
    """
    db.connect()
    db.drop_tables([User], safe=True)
    db.close()


# Ensure tables are created when running this script directly.
create_tables()
