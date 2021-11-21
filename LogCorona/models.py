from LogCorona import db
from peewee import (DateField, ForeignKeyField, Model, TextField)

database = db


class UnknownField(object):
    def __init__(self, *_, **__):
        pass


class BaseModel(Model):
    class Meta:
        database = database


class Peoples(BaseModel):
    first_name = TextField(null=True)
    last_name = TextField(null=True)
    people_id = TextField(primary_key=True)
    user_id = TextField(null=False)

    class Meta:
        table_name = 'peoples'


class Locations(BaseModel):
    location_id = TextField(primary_key=True)
    location_name = TextField(null=True)

    class Meta:
        table_name = 'locations'


class Users(BaseModel):
    last_name = TextField(column_name='last_name', null=True)
    password = TextField(column_name='password')
    username = TextField(column_name='username')
    create_date = DateField(null=True)
    first_name = TextField(null=True)
    user_id = TextField(primary_key=True)

    class Meta:
        table_name = 'users'


class CoronaLog(BaseModel):
    comments = TextField(null=True)
    create_date = DateField(null=True)
    location_id = ForeignKeyField(column_name='location_id', field='location_id', model=Locations, null=True)
    log_id = TextField(primary_key=True)
    people_id = ForeignKeyField(column_name='people_id', field='people_id', model=Peoples, null=True)
    user_id = ForeignKeyField(column_name='user_id', field='user_id', model=Users)

    class Meta:
        table_name = 'corona_log'


ALL_MODELS = BaseModel.__subclasses__()
