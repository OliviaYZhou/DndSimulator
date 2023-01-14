
from typing import Union, List, Optional
import sqlite3

def connect_to_db():
    conn = sqlite3.connect('test1.db')
    print("Opened database successfully")
    return conn


def init_db(conn):
    # conn.execute('''CREATE TABLE IF NOT EXISTS DICE(
    #  ID INT PRIMARY KEY NOT NULL,
    #  DICEMAX INT NOT NULL,
    #  DICEVAL INT NOT NULL
    #  );''')

    print("Table Dice created successfully")

def load_game(conn):
    cursor = get_from_db(conn, "DICE")
    for row in cursor:
        pass

def get_from_db(conn, table: str, values: Union[str, List]="ALL"):
    if values == "ALL":
        schema = conn.execute(f"SELECT * FROM pragma_table_info('{table}');")
        print("(" + " ".join([row[1] for row in schema]) + ")")
        cursor = conn.execute(f"SELECT * from {table} ORDER BY ID")
        return cursor
    else:
        if not type(values) == list:
            print("Values not list")
            return False
        cursor = conn.execute(f"SELECT {', '.join(values)} from {table}")
        print(" ".join(values))
        return cursor

def add_dice(conn, index, dicemax, diceval):
    conn.execute("""INSERT INTO DICE 
          VALUES (?,?,?);""", (index, dicemax, diceval))
    # conn.execute("""INSERT INTO DICE (INDEX,DICEMAX,DICEVAL) \
    #       VALUES (?,?,?);""", (index, dicemax, diceval))
    conn.commit()
    print("Dice added successfully")

def close_db(conn):
    conn.close()

def get_dicelist():
    conn = connect_to_db()
    cursor = get_from_db(conn, "DICE")
    dicelist = [[i[1], i[2]] for i in list(cursor)]

    print(dicelist)
    close_db(conn)
    return dicelist

def test_sqlite():
    
    conn = connect_to_db()
    # close_db(conn)
    # init_db(conn)

    cursor = get_from_db(conn, "DICE")
    dicelist = [[i[1], i[2]] for i in list(cursor)]

    print(dicelist)
    # add_skill(conn, 'Fireball-1', 1, 'FIREY', 2, '1d4', 'basic ball of fire')
    # add_skill(conn, 'Waterfall-3', 3, 'FIREY', 20, '2d20', 'big waterfall')
    # get_from_db(conn, "SKILLS")
    # close_db(conn)

    # conn = connect_to_db()
    # get_from_db(conn, "SKILLS")
    close_db(conn)


if __name__ == '__main__':
    test_sqlite()