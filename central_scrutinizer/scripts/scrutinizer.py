from peewee import *

database = MySQLDatabase('scrutinizer', **{'charset': 'utf8', 'sql_mode': 'PIPES_AS_CONCAT', 'use_unicode': True, 'user': 'kyclark', 'password': 'g0p3rl!'})

class UnknownField(object):
    def __init__(self, *_, **__): pass

class BaseModel(Model):
    class Meta:
        database = database

class LocationType(BaseModel):
    location_type = CharField(unique=True)
    location_type_id = AutoField()

    class Meta:
        table_name = 'location_type'

class Location(BaseModel):
    lat_lon = CharField(constraints=[SQL("DEFAULT ''")], null=True)
    location_id = AutoField()
    location_name = CharField(unique=True)
    location_type = ForeignKeyField(column_name='location_type_id', field='location_type_id', model=LocationType)

    class Meta:
        table_name = 'location'

class Medium(BaseModel):
    medium = CharField(unique=True)
    medium_id = AutoField()

    class Meta:
        table_name = 'medium'

class Source(BaseModel):
    source = CharField(unique=True)
    source_id = AutoField()

    class Meta:
        table_name = 'source'

class Variable(BaseModel):
    description = CharField(null=True)
    source = ForeignKeyField(column_name='source_id', field='source_id', model=Source)
    unit = CharField(constraints=[SQL("DEFAULT ''")], null=True)
    variable = CharField(unique=True)
    variable_id = AutoField()

    class Meta:
        table_name = 'variable'

class Measurement(BaseModel):
    collected_on = CharField(null=True)
    location = ForeignKeyField(column_name='location_id', field='location_id', model=Location)
    measurement_id = AutoField()
    medium = ForeignKeyField(column_name='medium_id', field='medium_id', model=Medium)
    value = FloatField()
    variable = ForeignKeyField(column_name='variable_id', field='variable_id', model=Variable)

    class Meta:
        table_name = 'measurement'
        indexes = (
            (('variable', 'location', 'medium', 'value'), True),
        )

