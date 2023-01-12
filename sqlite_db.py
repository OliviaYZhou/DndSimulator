from Skills import *
from Character import Character
from Dice import *
from typing import Union, List, Optional
import sqlite3


def load_game(conn):
    tables = ["CHARACTERS", "SKILLS", "ITEMS"]

    cursor = get_from_db(conn, "CHARACTERS")
    for row in cursor:
        pass

    cursor = get_from_db(conn, "SKILLS")
    for row in cursor:
        pass

    cursor = get_from_db(conn, "ITEMS")
    for row in cursor:
        pass

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
    # conn.execute('''CREATE TABLE SKILLS
    #          (ID               TEXT   PRIMARY KEY     NOT NULL,
    #           LEVEL            INT                   NOT NULL,
    #           NICKNAME         TEXT,
    #           BASE_EFFECT      INT,
    #           ROLL             TEXT,
    #           DESCRIPTION      TEXT);''')
    # print("Table Skill created successfully")

    conn.execute(
        '''CREATE TABLE BASIC_CHARACTER
           (ID               TEXT   PRIMARY KEY     NOT NULL,
            NAME             TEXT                   NOT NULL,        
            LEVEL            INT                    NOT NULL,
            GOLD             INT                    NOT NULL,
            EXP              INT                    NOT NULL);''')

    conn.execute(
        '''CREATE TABLE CHARACTER_STATS
           (
            CHARACTERID      TEXT   PRIMARY KEY     NOT NULL, 
            HP               INT                    NOT NULL,
            STR              INT                    NOT NULL,
            DEX              INT                    NOT NULL,
            CON              INT                    NOT NULL,
            INT              INT                    NOT NULL,
            WIS              INT                    NOT NULL,
            CHA              INT                    NOT NULL)
            ;''')
    conn.execute(
        '''CREATE TABLE STATUS_EFFECTS
           (STATUSID        INT PRIMARY KEY   AUTOINCREMENT,
            CHARACTERID     TEXT                   NOT NULL,        
            STAT            INT                    NOT NULL,
            AMOUNT          INT                    NOT NULL,
            DESCRIPTION     INT                    NOT NULL,
            DURATION        INT)                    
            ;''')
    print("Table Skill created successfully")

def get_from_db(conn, table:str, values:Union[str, List]="ALL"):
    if values == "ALL":
        schema = conn.execute(f"SELECT * FROM pragma_table_info('{table}');")
        print("(" + " ".join([row[1] for row in schema]) + ")")
        cursor = conn.execute(f"SELECT * from {table}")
        for row in cursor:
            print(row)
        return cursor
    else:
        if not type(values) == list:
            print("Values not list")
            return False
        cursor = conn.execute(f"SELECT {', '.join(values)} from {table}")
        print(" ".join(values))
        for row in cursor:
            print(row)
        return cursor



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

if __name__ == '__main__':
    test_sqlite()