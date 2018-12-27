import os
from peewee import *

from globals import development_mode

#  monster stats: name, type, spells, min_hp, max_hp, attack, speed, defense, algorithm, light_r, power
all_monsters = [
    ['goblin', 'ground', {'Projectile': ['Arrow']}, 1, 2, 1, 1, 1, 0, 5, 2],
    ['spider', 'ground', {'Melee': ['Bite']}, 1, 3, 2, 1, 3, 0, 2, 3],
    ['ogre', 'ground', {'Melee': ['Swing']}, 8, 15, 7, 1, 5, 0, 4, 8],
    ['vulture', 'flying', {'Melee': ['Claw']}, 7, 11, 8, 2, 2, 0, 15, 10],
    ['snake', 'ground',  {'Melee': ['Bite']}, 1, 1, 1, 1, 0, 0, 3, 0],
    ['cerberus', 'ground', {'Melee': ['Triple_Bite']}, 20, 25, 14, 3, 10, 0, 12, 30]
]

db_name = 'tables.db'
db = SqliteDatabase(db_name)


class MonsterTable(Model):
    id_field = PrimaryKeyField(primary_key=True)
    name = CharField(unique=True)
    type = CharField()  # ground or flying monster
    spells = TextField()
    min_hp = IntegerField(default=1)
    max_hp = IntegerField(default=1)
    attack = IntegerField(default=1)
    speed = IntegerField(default=1)
    defense = IntegerField(default=1)
    algorithm = IntegerField(default=0)
    light_r = IntegerField(default=1)
    power = IntegerField(default=1)

    class Meta:
        database = db

    @staticmethod
    def disconnect():
        db.close()


def clear():
    os.system('cls' if os.name == 'nt' else 'clear')


def initialize():
    """Create the database and the table if they don't exist."""

    try:
        os.remove(db_name)
    except OSError:
        pass
    db.connect()
    db.create_tables([MonsterTable], safe=True)
    # print('development')
    for monster in all_monsters:
        MonsterTable.create(name=monster[0], type=monster[1], spells=monster[2], min_hp=monster[3], max_hp=monster[4],
                            attack=monster[5], speed=monster[6], defense=monster[7], algorithm=monster[8],
                            light_r=monster[9], power=monster[10])
    return


if os.path.isfile(db_name) and not development_mode:
    # print('production')
    pass
else:
    initialize()

