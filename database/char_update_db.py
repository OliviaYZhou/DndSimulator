import math
import psycopg2
conn = psycopg2.connect("dbname=dndtoolkitdb user=olivia")

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

def lose_hp(charid, amount):
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

def recover_lost_hp(charid, amount):
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