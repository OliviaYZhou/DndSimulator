# This is a sample Python script.

# Press ⇧F10 to execute it or replace it with your code.
# Press Double ⇧ to search everywhere for classes, files, tool windows, actions, and settings.

from Skills import *
from Character import Character
from Dice import *
from typing import Union, List, Optional
import sqlite3


def load_game():
    pass
    # load game from database
def add_character():
    pass
def add_item():
    pass
def add_skill(conn, idd, level=0, nickname=None, base_effect=0, roll=None, description=""):
    conn.execute("""INSERT INTO SKILLS (ID,LEVEL,NICKNAME,BASE_EFFECT,ROLL,DESCRIPTION) \
          VALUES (?,?,?,?,?,?);""", (idd, level, nickname, base_effect, roll, description))
    conn.commit()
    print("Skill added successfully")

def connect_to_db():
    conn = sqlite3.connect('test1.db')
    print("Opened database successfully")
    return conn

def init_db(conn):
    conn.execute('''CREATE TABLE SKILLS
             (ID               TEXT   PRIMARY KEY     NOT NULL,
              LEVEL            INT                   NOT NULL,
              NICKNAME         TEXT,
              BASE_EFFECT      INT,
              ROLL             TEXT,
              DESCRIPTION      TEXT);''')
    print("Table Skill created successfully")

def get_from_db(conn, table:str, values:Union[str, List]="ALL"):
    if values == "ALL":
        schema = conn.execute(f"SELECT * FROM pragma_table_info('{table}');")
        print("(" + " ".join([row[1] for row in schema]) + ")")
        cursor = conn.execute(f"SELECT * from {table}")
        for row in cursor:
            print(row)
    else:
        if not type(values) == list:
            print("Values not list")
            return False
        cursor = conn.execute(f"SELECT {', '.join(values)} from {table}")
        for i in range(len(values)):
            print(" ".join(values))
            for row in cursor:
                print(row)



def close_db(conn):
    conn.close()


def test_sqlite():
    # conn = connect_to_db()
    # init_db(conn)
    # add_skill(conn, 'Fireball-1', 1, 'FIREY', 2, '1d4', 'basic ball of fire')
    # add_skill(conn, 'Waterfall-3', 3, 'FIREY', 20, '2d20', 'big waterfall')
    # get_from_db(conn, "SKILLS")
    # close_db(conn)

    conn = connect_to_db()
    get_from_db(conn, "SKILLS")
    close_db(conn)



def attack(skill: Skill, user: Character, target: Character):
    user_dex = user.get_stat("dex")
    target_dex = target.get_stat("dex")
    user_roll = input(f"{user.name} roll d20")
    target_roll = input(f"{target.name} roll d10")
    initiation = initiation_roll(user_dex, user_roll)
    defense = defense_roll(target_dex, target_roll)

    if initiation > defense:
        print("Attack Hits!!")
        target.damage_taken

def initiation_roll(dex, roll=None):
    if roll:
        return dex + roll
    else:
        print("Roll D20")
        auto_roll = d20()
        print(f"You got {auto_roll}")
        return dex+auto_roll

def defense_roll(dex, roll=None):
    if roll:
        return dex + roll
    else:
        print("Roll D10")
        auto_roll = d10()
        print(f"You got {auto_roll}")
        return dex+auto_roll

# def main_game_loop():
#     turn, characters, skills, items = load_game()
#     while turn:
#         turn += 1
# Press the green button in the gutter to run the script.
if __name__ == '__main__':
    test_sqlite()
    # main_game_loop()

# See PyCharm help at https://www.jetbrains.com/help/pycharm/
