from .database import AppModel, db_app, JSONField
from peewee import CharField


class AppConfig(AppModel):
    """
    Instrument sources.
    """
    key = CharField(max_length=32, index=True)
    value = JSONField()

def create_tables():
    """
    Create tables. If the table to be created already exists, it will be passed.
    Only necessary during initial.
    """
    model_list = [AppConfig]
    with db_app:
        db_app.create_tables(model_list, safe=True)
