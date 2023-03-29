try:    
    from database.db_functions import *
except ModuleNotFoundError:
    from db_functions import *
import psycopg2
conn = psycopg2.connect("dbname=dndtoolkitdb user=olivia")


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
    # cur = conn.cursor()
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
    # apparently this one provides the fucking name
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

    # q4 = """
    # SELECT NAME FROM BASIC_CHARACTER WHERE ID=(%s);
    # """
    # cur.execute(q4, (charid,))

    # name = cur.fetchone()[0]
    # current_stats = [max_stats[i] + status_effects[i] for i in range(7)]
    # "[hp: 40/100, str: 19 (20-1), etc"
    cur.close()
    return {"status_effects": status_effects, "max_stats":max_stats, "level": level} # , "name": name

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
        # important! player stats are never none nowadays
        return False
    player_stats["name"] = get_character_name(charid)
    inventory = get_character_inventory(charid)
    if not inventory["inventory"]:
        return player_stats
    player_stats["inventory"] = inventory["inventory"]
    
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
    return {"inventory": items_json_list}

def get_character_name(charid):
    cur = conn.cursor()
    q4 = """
    SELECT NAME FROM BASIC_CHARACTER WHERE ID=(%s);
    """
    cur.execute(q4, (charid,))

    name = cur.fetchone()[0]
    cur.close()
    return name