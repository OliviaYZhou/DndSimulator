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