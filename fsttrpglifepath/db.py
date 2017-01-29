from peewee import *
from fsttrpgcharloader.database import Actor, DBManager as ActorDBManager

lifepath_db = SqliteDatabase('lifepath.db')


class Event(Model):
    actor = ForeignKeyField(Actor, related_name='actors')
    year = IntegerField()
    month = IntegerField(default=1)
    length = IntegerField(default=1)
    event_chain = CharField()

    def add_event(self, actor_role, actor_name, year, event_chain, month=1, length=1):
        act = Actor.add_or_get(role=actor_role, name=actor_name)
        event, created = Event.get_or_create(actor=act,
                                             year=year,
                                             month=month,
                                             defaults={'event_chain': event_chain,
                                                       'length': length})
        if created:
            print('created new event')
            return True
        else:
            print('didnt create new event')
            return False

    class Meta:
        database = lifepath_db


class Enemy(Model):
    life_event = ForeignKeyField(Event, related_name='events')
    enemy_actor = ForeignKeyField(Actor, related_name='enemy_actors')
    relationship = CharField()
    resources = CharField()

    class Meta:
        database = lifepath_db


class DBManager(object):
    def __init__(self):
        self.actor_db_mgr = ActorDBManager()
        lifepath_db.connect()
        lifepath_db.create_tables([Event], safe=True)

        self.events = Event()

    def __del__(self):
        if lifepath_db:
            lifepath_db.close()
