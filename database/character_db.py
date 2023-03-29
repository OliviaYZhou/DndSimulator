import os
import psycopg2
import psycopg2.extras

try:
    from database.db_functions import *
    from database.char_get_db import *
    from database.char_insert_db import *
    from database.char_update_db import *
    from database.char_delete_db import *
except ModuleNotFoundError:
    from db_functions import *
    from char_get_db import *
    from char_insert_db import *
    from char_update_db import *
    from char_delete_db import *
from psycopg2 import sql



try:
    from __main__ import conn
except ImportError:
    try:
        print("main import failed")
        from server import conn
    except:
        print("server import failed")
        conn = psycopg2.connect("dbname=dndtoolkitdb user=olivia")


    
# def set_conn(connection = None):

#     global conn 
#     if not connection and not conn:
#         conn = psycopg2.connect("dbname=dndtoolkitdb user=olivia")
#     else:
#         conn = connection
# from psql_init import init_db


stat_order_list = ["HP", "STR", "DEX", "CON", "INT", "WIS", "CHA"]




# def update_HP(charid, amount):
#     cur = conn.cursor()
#     q1 = """
#     UPDATE CHARACTER_STATS SET LEVEL = (CHARACTER_STATS.LEVEL + (%s)) WHERE CHARACTERID=(%s);
#     """
#     cur.execute(q1, (amount, charid))
#     conn.commit()
#     cur.close()
#     print(f"{amount} levels added to {charid}")



def close_db(cur):
    cur.close()
    conn.close()

def close_cursor(cur):
    cur.close()
    
def save_db(connection = None, charid=None):
    if not connection:
        conn.commit()
        if charid:
            print(get_player_stats(charid))
    else:
        connection.commit()
    print("Database saved.")

# SELECT HP+MHP, STR+MSTR, DEX+MDEX, CON+MCON, INT+MINT, WIS+MWIS, CHA+MCHA 
# FROM CHARACTER_STATS, MSTATS
# WHERE CHARACTER_STATS.CHARACTERID = {charid};

# SELECT SUM(HP) AS MHP, SUM(STR) AS MSTR, SUM(DEX) AS MDEX, SUM(CON) AS MCON, SUM(INT) AS MINT, SUM(WIS) AS MWIS, SUM(CHA) AS MCHA
# FROM STATUS_EFFECTS WHERE CHARACTERID={CHARID};'''

# Insert data into the table

# cur.execute('INSERT INTO books (title, author, pages_num, review)'
#             'VALUES (%s, %s, %s, %s)',
#             ('A Tale of Two Cities',
#              'Charles Dickens',
#              489,
#              'A great classic!')
#             )

# cur.execute('INSERT INTO books (title, author, pages_num, review)'
#             'VALUES (%s, %s, %s, %s)',
#             ('Anna Karenina',
#              'Leo Tolstoy',
#              864,
#              'Another great classic!')
#             )
if __name__ == "__main__":
    # get_character_id_list()
    print(get_player_stats("tester3"))
    
    # psql_init.init_db(cur)
    # set_conn()
    # get_all_characters()
    
    # conn.commit()
    # print(get_player_stats("tester2"))




