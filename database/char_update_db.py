import math
import psycopg2
conn = psycopg2.connect("dbname=dndtoolkitdb user=olivia")

try:
    from database.db_functions import SESSION
    from database.char_insert_db import add_history
except ModuleNotFoundError:
    from db_functions import SESSION
    from char_insert_db import add_history


def update_gold(charid, amount, cause="", session=SESSION):
    cur = conn.cursor()
    q1 = """
    UPDATE CUMULATIVE_STATS SET GOLD = (CUMULATIVE_STATS.GOLD + (%s)) WHERE CHARACTERID=(%s);
    """
    cur.execute(q1, (amount, charid))
    conn.commit()
    cur.close()
    print(f"{amount} of gold added to {charid}")
    add_history(charid, "gold", amount, session, cause)


def update_exp(charid, amount, cause="", session=SESSION):
    print("update exp")
    cur = conn.cursor()
    q1 = """
    UPDATE CUMULATIVE_STATS SET EXP = (CUMULATIVE_STATS.EXP + (%s)) WHERE CHARACTERID=(%s);
    """
    cur.execute(q1, (amount, charid))
    conn.commit()
    cur.close()
    print(f"{amount} of exp added to {charid}")
    add_history(charid, "exp", amount, session, cause)

def update_level(charid, amount, cause="", session=SESSION):
    cur = conn.cursor()
    q1 = """
    UPDATE CHARACTER_STATS SET LEVEL = (CHARACTER_STATS.LEVEL + (%s)) WHERE CHARACTERID=(%s);
    """
    cur.execute(q1, (amount, charid))
    conn.commit()
    cur.close()
    print(f"{amount} levels added to {charid}")
    add_history(charid, "level", amount, session, cause)

def lose_hp(charid, amount, cause="", session=SESSION):
    # negative amount is positive lost hp
    amount = abs(amount)
    cur = conn.cursor()
    q1 = """
    UPDATE REGENERATIVE_STATS SET LOST_HP = (REGENERATIVE_STATS.LOST_HP + (%s)) WHERE CHARACTERID=(%s);
    """
    cur.execute(q1, (amount, charid))
    conn.commit()
    cur.close()
    print(f"{charid} hp - {amount}")
    add_history(charid, "hp", -amount, session, cause)

def recover_lost_hp(charid, amount, cause="", session=SESSION):
    # we work with positive amounts
    amount = abs(amount)
    cur = conn.cursor()
    q0 = """SELECT LOST_HP FROM REGENERATIVE_STATS WHERE CHARACTERID=(%s); """
    cur.execute(q0, (charid,))
    current_lost_hp = cur.fetchone()[0]
    if current_lost_hp < amount:
        amount = current_lost_hp
    
    q1 = """
    UPDATE REGENERATIVE_STATS SET LOST_HP = (REGENERATIVE_STATS.LOST_HP - (%s)) WHERE CHARACTERID=(%s);
    """
    cur.execute(q1, (amount, charid))
    conn.commit()
    cur.close()
    print(f"{charid} hp + {amount}")
    add_history(charid, "hp", amount, session, cause)