import psycopg2
conn = psycopg2.connect("dbname=dndtoolkitdb user=olivia")
try:
    from database.db_functions import SESSION, stat_order_list
except ModuleNotFoundError:
    from db_functions import SESSION, stat_order_list

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

        cur.execute('INSERT INTO REGENERATIVE_STATS (CHARACTERID, LOST_HP, LOST_MP) VALUES (%s, %s, %s)', (character_id, 0, 0))
    conn.commit()
    cur.close()
    print(f"Character stats of {character_id} added")



def add_status_effect(character_id, effect_name, stats, duration=1, description='', session=SESSION):
    cur = conn.cursor()
    list_effected_stats = []
    if type(stats) == str:
        list_stats = stats.split(" ")
        print(list_stats)
        cur.execute('INSERT INTO STATUS_EFFECTS (NAME, CHARACTERID, HP, STR, DEX, CON, INT, WIS, CHA, DESCRIPTION, DURATION, DURATION_REMAINING)'
        'VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s)', (effect_name, character_id, list_stats[0], list_stats[1],
        list_stats[2], list_stats[3], list_stats[4], list_stats[5], list_stats[6], description, duration, duration))
        print(f"Status effect {effect_name} added to {character_id}.")
        for i in range(7):
            if int(list_stats[i]) != 0:
                list_effected_stats.append({"affected": stat_order_list[i], "amount": int(list_stats[i])})
    elif type(stats) == dict:
        cur.execute('INSERT INTO STATUS_EFFECTS (NAME, CHARACTERID, HP, STR, DEX, CON, INT, WIS, CHA, DESCRIPTION, DURATION, DURATION_REMAINING)'
        'VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s)', (effect_name, character_id, stats["HP"], stats["STR"],
        stats["DEX"], stats["CON"], stats["INT"], stats["WIS"], stats["CHA"], description, duration, duration))
        print(f"Status effect {effect_name} added to {character_id}.")
        for stat in stat_order_list:
            if int(stats[stat]) != 0:
                list_effected_stats.append({"affected": stat, "amount": int(stats[stat])})

    conn.commit()
    cur.close()
    for affected_stat in list_effected_stats:
        add_history(character_id, affected_stat["affected"], affected_stat["amount"], session, f"{effect_name} | {description} | duration: {duration}")

def add_status_effect_delayed(character_id, effect_name, stats, duration, duration_remaining, description='', session=SESSION):
    cur = conn.cursor()
    list_effected_stats = []
    if type(stats) == str:
        list_stats = stats.split(" ")
        cur.execute('INSERT INTO STATUS_EFFECTS (NAME, CHARACTERID, HP, STR, DEX, CON, INT, WIS, CHA, DESCRIPTION, DURATION, DURATION_REMAINING)'
        'VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s)', (effect_name, character_id, list_stats[0], list_stats[1],
        list_stats[2], list_stats[3], list_stats[4], list_stats[5], list_stats[6], description, duration, duration_remaining))
        for i in range(7):
            if int(list_stats[i]) != 0:
                list_effected_stats.append({"affected": stat_order_list[i], "amount": int(list_stats[i])})
    conn.commit()
    cur.close()
    print(f"Status effect {effect_name} added to {character_id}.")
    for affected_stat in list_effected_stats:
        add_history(character_id, affected_stat["affected"], affected_stat["amount"], session, f"{effect_name} | {description} | duration: {duration}")

def add_cumulative_stats(character_id, gold, exp):
    cur = conn.cursor()
    cur.execute('INSERT INTO CUMULATIVE_STATS (CHARACTERID, GOLD, EXP)'
            'VALUES (%s, %s, %s)',(character_id, gold, exp))
    conn.commit()
    cur.close()
    print(f"Cumulative stats of {character_id} added")

def add_inventory_item(charid, item_name, amount, session=SESSION, description=''):
    cur = conn.cursor()
    print("add", charid, item_name, amount)


    q1 = """
    SELECT ITEM_NAME, AMOUNT FROM INVENTORY_ITEMS WHERE CHARACTERID=(%s) AND ITEM_NAME=(%s);
    """
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
    add_history(charid, item_name, amount, session, f"{amount} {item_name}(s) added to inventory; {description}")

# add to history table
def add_history(charid, affected, amount, session=SESSION, description=None):
    
    cur = conn.cursor()
    cur.execute('INSERT INTO HISTORY (CHARACTERID, AFFECTED, AMOUNT, SESSION, DESCRIPTION)'
            'VALUES (%s, %s, %s, %s, %s)', (charid, affected, amount, session, description))
    conn.commit()
    cur.close()
    amount = int(amount)
    amountstr = str(amount)
    if amount > 0:
        amountstr = "+" + amountstr
    print(f"History added: {charid} {affected} {amountstr} {description}")