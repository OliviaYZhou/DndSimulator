import psycopg2
from psycopg2 import sql
from character_db import *
from db_functions import SESSION, stat_order_list
def get_blocked_pids(conn):
    print("get blocked pids")
    cur = conn.cursor()
    q1 = """select pid, pg_blocking_pids(pid) as blocked_by, query as blocked_query
        from pg_stat_activity
        where pg_blocking_pids(pid)::text != '{}';"""
    cur.execute(q1)
    print(cur.fetchall())
    cur.close()
    print("finished blocked pids")

def terminate_blocks(conn, pids):
    print("terminate blocked pids")
    cur = conn.cursor()
    q1 = """SELECT pg_terminate_backend(%s);"""
    for i in pids:
        cur.execute(q1, (i,))
        print(f"terminated pid {i}")
    print("finished terminating blocks")

def alter_delete_cascade_CHARACTER_STATS(conn):
    print(f"start alter table CHARACTER_STATS")
    cur = conn.cursor()
    q1 = """ALTER TABLE CHARACTER_STATS
    DROP CONSTRAINT CHARACTER_STATS_CHARACTERID_FKEY,
    ADD CONSTRAINT CHARACTER_STATS_CHARACTERID_FKEY
        FOREIGN KEY (CHARACTERID)
        REFERENCES BASIC_CHARACTER(ID)
        ON DELETE CASCADE;"""
    cur.execute(q1)
    cur.close()
    conn.commit()
    print(f"altered CHARACTER_STATS")

def alter_delete_cascade_CUMULATIVE_STATS(conn):
    print(f"start alter table CUMULATIVE_STATS")
    cur = conn.cursor()
    q1 = """ALTER TABLE CUMULATIVE_STATS
    DROP CONSTRAINT CUMULATIVE_STATS_CHARACTERID_FKEY,
    ADD CONSTRAINT CUMULATIVE_STATS_CHARACTERID_FKEY
        FOREIGN KEY (CHARACTERID)
        REFERENCES BASIC_CHARACTER(ID)
        ON DELETE CASCADE;"""
    cur.execute(q1)
    cur.close()
    conn.commit()
    print(f"altered CUMULATIVE_STATS")

def alter_delete_cascade_STATUS_EFFECTS(conn):
    print(f"start alter table STATUS_EFFECTS")
    cur = conn.cursor()
    q1 = """ALTER TABLE STATUS_EFFECTS
    DROP CONSTRAINT STATUS_EFFECTS_CHARACTERID_FKEY,
    ADD CONSTRAINT STATUS_EFFECTS_CHARACTERID_FKEY
        FOREIGN KEY (CHARACTERID)
        REFERENCES BASIC_CHARACTER(ID)
        ON DELETE CASCADE;"""
    cur.execute(q1)
    cur.close()
    conn.commit()
    print(f"altered STATUS_EFFECTS")


def alter_delete_cascade_INVENTORY_ITEMS(conn):
    print(f"start alter table INVENTORY_ITEMS")
    cur = conn.cursor()
    q1 = """ALTER TABLE INVENTORY_ITEMS
    DROP CONSTRAINT INVENTORY_ITEMS_CHARACTERID_FKEY,
    ADD CONSTRAINT INVENTORY_ITEMS_CHARACTERID_FKEY
        FOREIGN KEY (CHARACTERID)
        REFERENCES BASIC_CHARACTER(ID)
        ON DELETE CASCADE;"""
    cur.execute(q1)
    cur.close()
    conn.commit()
    print(f"altered INVENTORY_ITEMS")

def alter_delete_cascades(conn):

    # for all tables with foreign key charid
    # on delete cascade

    alter_delete_cascade_CHARACTER_STATS(conn)
    alter_delete_cascade_CUMULATIVE_STATS(conn)
    alter_delete_cascade_INVENTORY_ITEMS(conn)
    alter_delete_cascade_STATUS_EFFECTS(conn)

# populate history table with existing data from status_effects and inventory_items
# cumulative_stats will be added manually
def populate_history(conn):
    print("start populate history")
    cur = conn.cursor(cursor_factory = psycopg2.extras.RealDictCursor)

    q0 = """SELECT * FROM STATUS_EFFECTS;"""
    cur.execute(q0)
    for row in cur.fetchall():
        for stat_index in range(7):
            status_stat_amount = row[stat_order_list_lower[stat_index]]
            if status_stat_amount != 0:
                add_history(row["characterid"], stat_order_list[stat_index], status_stat_amount, 0, f"{row['name']}, duration: {row['duration']} | {row['description']}") # characterid, affected, amount, session, description
    q1 = """SELECT * FROM INVENTORY_ITEMS;"""
    cur.execute(q1)
    for row in cur.fetchall():
        add_history(row["characterid"], row["item_name"], row["amount"], 0, "Inventory") # characterid, affected, amount, session, description

    cur.close()
    conn.commit()
    print("finished populate history")

if __name__ == '__main__':
    print("run psql scripts")
    conn = psycopg2.connect("dbname=dndtoolkitdb user=olivia")
    print("connected")
    populate_history(conn)
    # get_blocked_pids(conn)
    # print(get_column_query("str", "status_effects"))
    # terminate_blocks(conn, [99900, 99012])
    # alter_delete_cascades(conn)
