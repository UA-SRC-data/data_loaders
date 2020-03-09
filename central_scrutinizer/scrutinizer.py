from peewee import *

database = SqliteDatabase('scrutinizer.db')

class UnknownField(object):
    def __init__(self, *_, **__): pass

class BaseModel(Model):
    class Meta:
        database = database

class LocationType(BaseModel):
    location_type = TextField(unique=True)
    location_type_id = AutoField(null=True)

    class Meta:
        table_name = 'location_type'

class Location(BaseModel):
    location_id = AutoField(null=True)
    location_name = TextField(unique=True)
    location_type = ForeignKeyField(column_name='location_type_id', field='location_type_id', model=LocationType)

    class Meta:
        table_name = 'location'

class Variable(BaseModel):
    description = TextField(null=True)
    variable = TextField(unique=True)
    variable_id = AutoField(null=True)

    class Meta:
        table_name = 'variable'

class Measurement(BaseModel):
    location = ForeignKeyField(column_name='location_id', field='location_id', model=Location)
    measurement_id = AutoField(null=True)
    value = TextField()
    variable = ForeignKeyField(column_name='variable_id', field='variable_id', model=Variable)

    class Meta:
        table_name = 'measurement'
        indexes = (
            (('variable', 'location', 'value'), True),
        )

