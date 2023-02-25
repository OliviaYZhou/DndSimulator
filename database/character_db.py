import os
import psycopg2
import psycopg2.extras


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
    
default_return = {"status": True}
failed_return = {"status": False}

def print_block(info, name=""):
    print("\n\n\n", name, info, "\n\n\n")
    
def set_conn(connection = None):

    global conn 
    if not connection and not conn:
        conn = psycopg2.connect("dbname=dndtoolkitdb user=olivia")
    else:
        conn = connection
# from psql_init import init_db


stat_order_list = ["HP", "STR", "DEX", "CON", "INT", "WIS", "CHA"]

def to_json(order_list, query_results):
    # print_block(query_results, "query_results")
    try:
        newJson = {}
        if query_results is None or query_results[0] is None:
            print_block("query results is None")
            
            for i in range(len(order_list)):
                newJson[order_list[i]] = 0
        else:
            for i in range(len(order_list)):
                newJson[order_list[i]] = query_results[i]
        return newJson
    except TypeError:
        return False


def add_character(character_id, name, character_type):
    cur = conn.cursor()
    cur.execute('INSERT INTO BASIC_CHARACTER (ID, NAME, CHARACTER_TYPE)'
            'VALUES (%s, %s, %s)',(character_id, name,character_type))
    conn.commit()
    cur.close()
    print(f"Character {character_id} added")

def add_character_stats(character_id, stats, level):
    cur = conn.cursor()
    if type(stats) == str:
        list_stats = stats.split(" ")
        cur.execute('INSERT INTO CHARACTER_STATS (CHARACTERID, LEVEL, HP, STR, DEX, CON, INT, WIS, CHA)'
        'VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s)', (character_id, level, list_stats[0], list_stats[1],
        list_stats[2], list_stats[3], list_stats[4], list_stats[5], list_stats[6]))
    conn.commit()
    cur.close()
    print(f"Character stats of {character_id} added")

def format_single_stat_status_effect(stat, amount):
    stat_chosen = stat.upper()
    stat_string = ''
    for i in range(len(stat_order_list)):
        if stat_order_list[i] == stat_chosen:
            stat_string += f' {amount}'
            stat_string += " 0"*(len(stat_order_list)-i-1)
            break
        else:
            stat_string += " 0"
    
    return stat_string[1:]

def add_status_effect(character_id, effect_name, stats, duration=1, description=''):
    cur = conn.cursor()

    if type(stats) == str:
        list_stats = stats.split(" ")
        print(list_stats)
        cur.execute('INSERT INTO STATUS_EFFECTS (NAME, CHARACTERID, HP, STR, DEX, CON, INT, WIS, CHA, DESCRIPTION, DURATION, DURATION_REMAINING)'
        'VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s)', (effect_name, character_id, list_stats[0], list_stats[1],
        list_stats[2], list_stats[3], list_stats[4], list_stats[5], list_stats[6], description, duration, duration))
        print(f"Status effect {effect_name} added to {character_id}.")
    elif type(stats) == dict:
        cur.execute('INSERT INTO STATUS_EFFECTS (NAME, CHARACTERID, HP, STR, DEX, CON, INT, WIS, CHA, DESCRIPTION, DURATION, DURATION_REMAINING)'
        'VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s)', (effect_name, character_id, stats["HP"], stats["STR"],
        stats["DEX"], stats["CON"], stats["INT"], stats["WIS"], stats["CHA"], description, duration, duration))
        print(f"Status effect {effect_name} added to {character_id}.")
    conn.commit()
    cur.close()
    

def add_status_effect_delayed(character_id, effect_name, stats, duration, duration_remaining, description=''):
    cur = conn.cursor()
    if type(stats) == str:
        list_stats = stats.split(" ")
        cur.execute('INSERT INTO STATUS_EFFECTS (NAME, CHARACTERID, HP, STR, DEX, CON, INT, WIS, CHA, DESCRIPTION, DURATION, DURATION_REMAINING)'
        'VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s)', (effect_name, character_id, list_stats[0], list_stats[1],
        list_stats[2], list_stats[3], list_stats[4], list_stats[5], list_stats[6], description, duration, duration_remaining))
    conn.commit()
    cur.close()
    print(f"Status effect {effect_name} added to {character_id}.")

def add_cumulative_stats(character_id, gold, exp):
    cur = conn.cursor()
    cur.execute('INSERT INTO CUMULATIVE_STATS (CHARACTERID, GOLD, EXP)'
            'VALUES (%s, %s, %s)',(character_id, gold, exp))
    conn.commit()
    cur.close()
    print(f"Cumulative stats of {character_id} added")

def add_inventory_item(charid, item_name, amount):
    cur = conn.cursor()
    q1 = """
    SELECT ITEM_NAME, AMOUNT FROM INVENTORY_ITEMS WHERE CHARACTERID=(%s) AND ITEM_NAME=(%s);
    """
    print("add", charid, item_name, amount)
    cur.execute(q1, (charid, item_name))
    this_item = cur.fetchone()
    if not this_item:
        cur.execute('INSERT INTO INVENTORY_ITEMS (ITEM_NAME, CHARACTERID, AMOUNT)'
            'VALUES (%s, %s, %s)',(item_name, charid, amount))
    else:
        cur.execute('UPDATE INVENTORY_ITEMS SET AMOUNT = (INVENTORY_ITEMS.AMOUNT + (%s)) WHERE CHARACTERID=(%s) AND ITEM_NAME=(%s);'
        , (amount, charid, item_name))
    
    conn.commit()
    cur.close()
    print(f"{amount} of {item_name} added to inventory of {charid}")

def update_gold(charid, amount):
    cur = conn.cursor()
    q1 = """
    UPDATE CUMULATIVE_STATS SET GOLD = (CUMULATIVE_STATS.GOLD + (%s)) WHERE CHARACTERID=(%s);
    """
    cur.execute(q1, (amount, charid))
    conn.commit()
    cur.close()
    print(f"{amount} of gold added to {charid}")

def update_exp(charid, amount):
    print("update exp")
    cur = conn.cursor()
    q1 = """
    UPDATE CUMULATIVE_STATS SET EXP = (CUMULATIVE_STATS.EXP + (%s)) WHERE CHARACTERID=(%s);
    """
    cur.execute(q1, (amount, charid))
    conn.commit()
    cur.close()
    print(f"{amount} of exp added to {charid}")

def update_level(charid, amount):
    cur = conn.cursor()
    q1 = """
    UPDATE CHARACTER_STATS SET LEVEL = (CHARACTER_STATS.LEVEL + (%s)) WHERE CHARACTERID=(%s);
    """
    cur.execute(q1, (amount, charid))
    conn.commit()
    cur.close()
    print(f"{amount} levels added to {charid}")

# def update_HP(charid, amount):
#     cur = conn.cursor()
#     q1 = """
#     UPDATE CHARACTER_STATS SET LEVEL = (CHARACTER_STATS.LEVEL + (%s)) WHERE CHARACTERID=(%s);
#     """
#     cur.execute(q1, (amount, charid))
#     conn.commit()
#     cur.close()
#     print(f"{amount} levels added to {charid}")

def get_character_id_list():
    cur = conn.cursor()
    cur.execute("""
        SELECT ID FROM BASIC_CHARACTER
        """)
    id_tuples = cur.fetchall()
    id_list = [t[0] for t in id_tuples]
    cur.close()
    print_block(id_list)
    return id_list

def get_all_characters():
    cur = conn.cursor()
    cur = conn.cursor(cursor_factory = psycopg2.extras.RealDictCursor)
    cur.execute("""
    SELECT * FROM BASIC_CHARACTER
    """)
    print_block(cur.fetchall())
    cur.execute("""
    SELECT * FROM CHARACTER_STATS
    """)
    print_block(cur.fetchall())

    cur.execute("""
    SELECT * FROM STATUS_EFFECTS
    """)
    print_block(cur.fetchall())
    cur.close()

def get_character_stats(charid):
    
    cur = conn.cursor()

    q1 = '''
        SELECT SUM(HP), SUM(STR), SUM(DEX), SUM(CON), SUM(INT), SUM(WIS), SUM(CHA)
        FROM STATUS_EFFECTS WHERE CHARACTERID=(%s);'''
    print("characterid", charid)
    cur.execute(q1, (charid,))
    status_effects = (0,0,0,0,0,0,0)
    try:
        status_effects_placeholder = cur.fetchone()
        if status_effects_placeholder is None or status_effects_placeholder[0] is None:
            pass
        else:
            status_effects = status_effects_placeholder
    except psycopg2.ProgrammingError:
        print("not found")
    status_effects = to_json(stat_order_list, status_effects)
    # print(status_effects)

    q2 = '''
    SELECT HP, STR, DEX, CON, INT, WIS, CHA FROM CHARACTER_STATS WHERE CHARACTERID=(%s);
    '''
    cur.execute(q2, (charid,))

    max_stats = (0,0,0,0,0,0,0)
    try:
        max_stats = cur.fetchone()
        print_block(max_stats, "max_stats")
        if max_stats is None:
            return False
    except psycopg2.ProgrammingError:
        print_block("max_stats not found")
    
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
    cur.close()
    return {"status_effects": status_effects, "max_stats":max_stats, "level": level, "name": name}

def get_player_stats(charid):
    # print(charid)
    # print("get_player_stats", charid)
    stats_dict = get_character_stats(charid)
    # print(stats_dict)
    if stats_dict == False:
        
        print("character stats not found")
        stats_dict = to_json(stat_order_list, (-1,-1,-1,-1,-1,-1,-1))

    q1 = '''
    SELECT GOLD, EXP
    FROM CUMULATIVE_STATS WHERE CHARACTERID=(%s);'''

    cur = conn.cursor(cursor_factory = psycopg2.extras.RealDictCursor)
    cur.execute(q1, (charid,))
    cumulative_stats = cur.fetchone()
    # print("cumulative_stats", cumulative_stats)
    # cumulative_stats = to_json(["gold", "exp"], cumulative_stats)
    
    stats_dict["gold"] = 0
    stats_dict["exp"] = 0
    if cumulative_stats is not None:
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
    # print(status_breakdown)
    stats_dict["stat_breakdown"] = status_breakdown
    cur.close()
    return stats_dict

def get_all_player_info(charid):
    # print("playerinfo")
    player_stats = get_player_stats(charid)
    if not player_stats:
        print("player stats not found")
        return False
    inventory = get_character_inventory(charid)
    if not inventory:
        return player_stats
    player_stats["inventory"] = inventory
    return player_stats
  
def get_status_effects_of(statQuery, charid, verbose=False):
    # cur = conn.cursor(cursor_factory = psycopg2.extras.RealDictCursor)
    # q1 = sql.SQL("""SELECT "WIS" FROM STATUS_EFFECTS WHERE CHARACTERID=(%s) AND WIS != 0""")
    # q1 = sql.SQL("""SELECT {}, NAME, DESCRIPTION, DURATION, DURATION_REMAINING FROM STATUS_EFFECTS WHERE CHARACTERID=(%s) AND {} != 0""").format(sql.Identifier(stat), sql.Identifier(stat))
    q1 = statQuery
    cur = conn.cursor()
    cur.execute(q1,  (charid,))
    status_effects_tuple_list = cur.fetchall()
    if status_effects_tuple_list is None:
        return []
    if verbose:
        print("status_effects_tuple_list", status_effects_tuple_list)
    status_effects_json_list = []
    for row in status_effects_tuple_list:
        status_effects_json_list.append(to_json(["AMOUNT", "NAME", "DESCRIPTION", "DURATION", "DURATION_REMAINING"], row))
    cur.close()
    return status_effects_json_list

def get_basic_character(charid):
    
    cur = conn.cursor()
    q1 = '''SELECT * FROM BASIC_CHARACTER WHERE ID=(%s);'''
    # print("characterid", charid)
    cur.execute(q1,  (charid,))

    basic_character_tuple = cur.fetchone()
    character_json = to_json(["characterid", "name", "character_type"], basic_character_tuple)
    return character_json 
    

def get_character_inventory(charid, verbose=False):
    cur = conn.cursor()
    q1 = """
    SELECT ITEM_NAME, AMOUNT FROM INVENTORY_ITEMS WHERE CHARACTERID=(%s);
    """
    cur.execute(q1, (charid,))

    all_items = cur.fetchall()

    items_json_list = []
    for item_tuple in all_items:
        items_json_list.append(to_json(["itemName", "amount"], item_tuple))

    cur.close()
    if verbose:
        print("inventory", items_json_list)
    return items_json_list

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




