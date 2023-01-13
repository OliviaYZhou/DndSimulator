import os
import psycopg2
import psycopg2.extras
from psycopg2 import sql
import psql_init

conn = psycopg2.connect("dbname=dndtoolkitdb user=olivia")
stat_order_list = ["HP", "STR", "DEX", "CON", "INT", "WIS", "CHA"]
# Open a cursor to perform database operations
cur = conn.cursor()

def add_character(character_id, name, character_type):
    cur.execute('INSERT INTO BASIC_CHARACTER (ID, NAME, CHARACTER_TYPE)'
            'VALUES (%s, %s, %s)',(character_id, name,character_type))
    conn.commit()

def add_character_stats(character_id, stats, level):
    if type(stats) == str:
        list_stats = stats.split(" ")
        cur.execute('INSERT INTO CHARACTER_STATS (CHARACTERID, LEVEL, HP, STR, DEX, CON, INT, WIS, CHA)'
        'VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s)', (character_id, level, list_stats[0], list_stats[1],
        list_stats[2], list_stats[3], list_stats[4], list_stats[5], list_stats[6]))
    conn.commit()

def add_status_effect(character_id, stats, effect_name , description='', duration=1):
    if type(stats) == str:
        list_stats = stats.split(" ")
        cur.execute('INSERT INTO STATUS_EFFECTS (NAME, CHARACTERID, HP, STR, DEX, CON, INT, WIS, CHA, DESCRIPTION, DURATION, DURATION_REMAINING)'
        'VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s)', (effect_name, character_id, list_stats[0], list_stats[1],
        list_stats[2], list_stats[3], list_stats[4], list_stats[5], list_stats[6], description, duration, duration))
    conn.commit()

def add_cumulative_stats(character_id, gold, exp):
    cur.execute('INSERT INTO CUMULATIVE_STATS (CHARACTERID, GOLD, EXP)'
            'VALUES (%s, %s, %s)',(character_id, gold, exp))
    conn.commit()

def get_all_characters():
    cur = conn.cursor(cursor_factory = psycopg2.extras.RealDictCursor)
    cur.execute("""
    SELECT * FROM BASIC_CHARACTER
    """)
    print(cur.fetchall())
    cur.execute("""
    SELECT * FROM CHARACTER_STATS
    """)
    print(cur.fetchall())

    cur.execute("""
    SELECT * FROM STATUS_EFFECTS
    """)
    print(cur.fetchall())

def get_character_stats(charid):

    q1 = '''
        SELECT SUM(HP), SUM(STR), SUM(DEX), SUM(CON), SUM(INT), SUM(WIS), SUM(CHA)
        FROM STATUS_EFFECTS WHERE CHARACTERID=(%s);'''

    cur.execute(q1, (charid,))
    status_effects = cur.fetchone()
    status_effects = to_json(stat_order_list, status_effects)
    # print(status_effects)

    q2 = '''
    SELECT HP, STR, DEX, CON, INT, WIS, CHA FROM CHARACTER_STATS WHERE CHARACTERID=(%s);
    '''
    cur.execute(q2, (charid,))
    max_stats = cur.fetchone()
    # print(max_stats)
    max_stats = to_json(stat_order_list, max_stats)

    q3 = """
    SELECT LEVEL FROM CHARACTER_STATS WHERE CHARACTERID=(%s);
    """
    cur.execute(q3, (charid,))

    level = cur.fetchone()[0]

    q4 = """
    SELECT NAME FROM BASIC_CHARACTER WHERE ID=(%s);
    """
    cur.execute(q4, (charid,))

    name = cur.fetchone()[0]
    # current_stats = [max_stats[i] + status_effects[i] for i in range(7)]
    # "[hp: 40/100, str: 19 (20-1), etc"
    return {"status_effects": status_effects, "max_stats":max_stats, "level": level, "name": name}

def get_player_stats(charid):
    cur = conn.cursor(cursor_factory = psycopg2.extras.RealDictCursor)

    stats_dict = get_character_stats(charid)
    q1 = '''
    SELECT GOLD, EXP
    FROM CUMULATIVE_STATS WHERE CHARACTERID=(%s);'''

    cur.execute(q1, (charid,))
    cumulative_stats = cur.fetchone()
    # cumulative_stats = to_json(["gold", "exp"], cumulative_stats)

    stats_dict["gold"] = cumulative_stats["gold"]
    stats_dict["exp"] = cumulative_stats["exp"]

    stat_queries = [
        """SELECT HP, NAME, DESCRIPTION, DURATION, DURATION_REMAINING FROM STATUS_EFFECTS WHERE CHARACTERID=(%s) AND HP != 0""",
        """SELECT STR, NAME, DESCRIPTION, DURATION, DURATION_REMAINING FROM STATUS_EFFECTS WHERE CHARACTERID=(%s) AND STR != 0""",
        """SELECT DEX, NAME, DESCRIPTION, DURATION, DURATION_REMAINING FROM STATUS_EFFECTS WHERE CHARACTERID=(%s) AND DEX != 0""",
        """SELECT CON, NAME, DESCRIPTION, DURATION, DURATION_REMAINING FROM STATUS_EFFECTS WHERE CHARACTERID=(%s) AND CON != 0""",
        """SELECT INT, NAME, DESCRIPTION, DURATION, DURATION_REMAINING FROM STATUS_EFFECTS WHERE CHARACTERID=(%s) AND INT != 0""",
        """SELECT WIS, NAME, DESCRIPTION, DURATION, DURATION_REMAINING FROM STATUS_EFFECTS WHERE CHARACTERID=(%s) AND WIS != 0""",
        """SELECT CHA, NAME, DESCRIPTION, DURATION, DURATION_REMAINING FROM STATUS_EFFECTS WHERE CHARACTERID=(%s) AND CHA != 0""",
    ]
    status_breakdown = {}
    for i in range(7):
        status_breakdown[stat_order_list[i]] = get_status_effects_of(stat_queries[i], charid)
    print(status_breakdown)
    stats_dict["stat_breakdown"] = status_breakdown
    return stats_dict

  
def get_status_effects_of(statQuery, charid):
    # cur = conn.cursor(cursor_factory = psycopg2.extras.RealDictCursor)
    # q1 = sql.SQL("""SELECT "WIS" FROM STATUS_EFFECTS WHERE CHARACTERID=(%s) AND WIS != 0""")
    # q1 = sql.SQL("""SELECT {}, NAME, DESCRIPTION, DURATION, DURATION_REMAINING FROM STATUS_EFFECTS WHERE CHARACTERID=(%s) AND {} != 0""").format(sql.Identifier(stat), sql.Identifier(stat))
    q1 = statQuery
    cur.execute(q1,  (charid,))
    status_effects_tuple_list = cur.fetchall()
    # print(1, status_effects_tuple_list)
    status_effects_json_list = []
    for row in status_effects_tuple_list:
        status_effects_json_list.append(to_json(["AMOUNT", "NAME", "DESCRIPTION", "DURATION", "DURATION_REMAINING"], row))
    return status_effects_json_list


def to_json(order_list, query_results):
    newJson = {}
    for i in range(len(order_list)):
        newJson[order_list[i]] = query_results[i]
    return newJson

def close_db():
    cur.close()
    conn.close()

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
    # psql_init.init_db(cur)
    # add_character("tester2", "olivia2", "ncp")
    # add_character_stats("tester2", "20 5 6 7 8 9 10", 1)
    # add_status_effect("tester2", "0 0 0 0 -1 0 0", "Crushed Spirit", "From working in factory", 5)
    # add_status_effect("tester2", "0 0 0 0 0 -5 0", "Tired", "Loss of sleep", 1)
    # add_status_effect("tester2", "0 0 0 0 0 1 0", "Candy", "energizing candy", 1)


    # get_all_characters()
    # print(get_character_stats("tester2"))
    # add_cumulative_stats("tester2", 50, 300)
    # conn.commit()
    print(get_player_stats("tester2"))




