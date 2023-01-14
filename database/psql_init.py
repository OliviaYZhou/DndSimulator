from character_db import *

stat_order_list = ["HP", "STR", "DEX", "CON", "INT", "WIS", "CHA"]

def create_table_BASIC_CHARACTER(cur):
    cur.execute('DROP TABLE IF EXISTS BASIC_CHARACTER CASCADE;')
    cur.execute(
        '''CREATE TABLE BASIC_CHARACTER
        (ID              TEXT                PRIMARY KEY,
        NAME             TEXT,
        CHARACTER_TYPE   TEXT);''')  # player, npc, enemy
    print("Table BASIC_CHARACTER added")

def create_table_CHARACTER_STATS(cur):
    cur.execute('DROP TABLE IF EXISTS CHARACTER_STATS CASCADE;')
    cur.execute(
        '''CREATE TABLE CHARACTER_STATS
        (
        CHARACTERID      TEXT        PRIMARY KEY   REFERENCES BASIC_CHARACTER, 
        LEVEL            INTEGER,
        HP               INTEGER,
        STR              INTEGER,
        DEX              INTEGER,
        CON              INTEGER,
        INT              INTEGER,
        WIS              INTEGER,
        CHA              INTEGER);''')
    print("Table CHARACTER_STATS added")

def create_table_CUMULATIVE_STATS(cur):
    cur.execute('DROP TABLE IF EXISTS CUMULATIVE_STATS CASCADE;')
    cur.execute(

        '''CREATE TABLE CUMULATIVE_STATS
        (
        CHARACTERID      TEXT   PRIMARY KEY REFERENCES BASIC_CHARACTER,
        GOLD             INTEGER,
        EXP              INTEGER);''')
    print("Table CUMULATIVE_STATS added")

def create_table_STATUS_EFFECTS(cur):
    cur.execute('DROP TABLE IF EXISTS STATUS_EFFECTS CASCADE;')
    cur.execute(
        '''CREATE TABLE STATUS_EFFECTS
            (STATUSID       SERIAL   PRIMARY KEY,
            NAME            TEXT,
            CHARACTERID     TEXT     REFERENCES BASIC_CHARACTER,   
            HP              INTEGER,     
            STR             INTEGER,
            DEX             INTEGER,
            CON             INTEGER,
            INT             INTEGER,
            WIS             INTEGER,
            CHA             INTEGER,
            DESCRIPTION     TEXT,
            DURATION        INTEGER,
            DURATION_REMAINING INTEGER )                    
            ;''')
    print("Table STATUS_EFFECTS added")

def create_table_INVENTORY_ITEMS(cur):
    cur.execute('DROP TABLE IF EXISTS INVENTORY_ITEMS CASCADE;')

    cur.execute(
        '''CREATE TABLE INVENTORY_ITEMS
            (ITEM_NAME      TEXT      PRIMARY KEY,
            CHARACTERID     TEXT      NOT NULL REFERENCES BASIC_CHARACTER, 
            AMOUNT          INTEGER                NOT NULL)                    
            ;''')
    print("Table INVENTORY_ITEMS added")

def create_table_ITEMS(cur):
    cur.execute('DROP TABLE IF EXISTS ITEMS CASCADE;')
    cur.execute(
    '''CREATE TABLE ITEMS
        (ITEMID         SERIAL   PRIMARY KEY,
        ITEMNAME        TEXT                   NOT NULL,        
        DESCRIPTION     INTEGER,
        EFFECTID        INTEGER)                    
        ;''')
    print("Table ITEMS added")
    
def create_table_SKILLS(cur):
    cur.execute('DROP TABLE IF EXISTS SKILLS;')

    cur.execute(
        '''CREATE TABLE SKILLS
            (SKILLID       SERIAL   PRIMARY KEY,
            NAME           TEXT                   NOT NULL,        
            LEVEL          TEXT                   NOT NULL,
            BASE           INT,
            MAXROLL        INT,
            DESCRIPTION    INTEGER)                    
            ;''')
    print("Table SKILLS added")

def add_player_character(characterid, name, stats, level, gold, exp):
    add_character(characterid, name, "player")
    add_character_stats(characterid, stats, level)
    add_cumulative_stats(characterid, gold, exp)

    print(f"Player character {characterid} added.")


def init_db(cur, conn):
    create_table_BASIC_CHARACTER(cur)
    create_table_CHARACTER_STATS(cur)
    create_table_CUMULATIVE_STATS(cur)
    create_table_STATUS_EFFECTS(cur)
    create_table_INVENTORY_ITEMS(cur)
    # create_table_ITEMS(cur)
    # create_table_SKILLS(cur)

    save_db(conn)

def init_tentacle_guy():
    add_player_character("tentacle_guy", "Justice", "9 12 15 11 13 11 14", 1, 11, 20)
    add_status_effect_delayed("tentacle_guy", "Public WC", format_single_stat_status_effect("dex", 1), 6, 3, "Using it makes you feel refreshed.")
    add_status_effect_delayed("tentacle_guy", "Calomornorioguraomne Chocolate", format_single_stat_status_effect("con", 1), 6, 3, "Candy from the confectionery shop. Tentacle guy likes chocolate.")
    add_status_effect_delayed("tentacle_guy", "Tiny Babbit Milk Candy", format_single_stat_status_effect("wis", -1), 6, 3, "Candy from the confectionery shop. Tentacle guy did not like it.")
    add_status_effect_delayed("tentacle_guy", "Sniggers Reanut Filled Chocolates", format_single_stat_status_effect("int", 1), 6, 3, "Candy from the confectionery shop. Tentacle guy likes chocolate.")

    add_status_effect_delayed("tentacle_guy", "Unpasturized Milk", format_single_stat_status_effect("str", -1), 6, 3, "You drank an entire bucket. Be grateful you're immune to food poisoning.")
    add_status_effect_delayed("tentacle_guy", "Milk", format_single_stat_status_effect("con", 5), 6, 3, "You drank an entire bucket. It is good for the bones.")
    print(get_player_stats("tentacle_guy"))

def init_orc_guy():
    add_player_character("orc_guy", "Bulbophyllum", "7 12 11 16 10 9 8", 1, 0, 0)
    add_status_effect_delayed("orc_guy", "Fountain Water", format_single_stat_status_effect("int", -1), 6, 3, "Don't drink too many ingredients you can't pronounce.")
    add_status_effect_delayed("orc_guy", "Aspirational Ambition", "0 3 0 3 1 0 0", 7, 4, 'After reading "One Day, They Shall Kneel Before Me" by DragonSlayer420, \
    you feel a heat inside you that can only be described as pure draconic ambition')
    add_status_effect_delayed("orc_guy", 'Bulk Energy "Potion"', format_single_stat_status_effect("str", 1), 3, 2, 'You feel slightly less sleepy. Maybe.')
    add_status_effect_delayed("orc_guy", "Shattered Dreams", "0 0 0 0 -3 -3 0", 6, 3, 'After just one day working in the factory, you feel your dreams fade in front of \
    you as you become occupied by little more than the next task in front of you')
    add_status_effect_delayed("orc_guy", "Ruined Hands", format_single_stat_status_effect("str", -3), 6, 3, 'You spent 3 hours flipping through weapons with your bare hands. \
    You are exhausted.')
    print(get_player_stats("orc_guy"))

if __name__ == '__main__':
    conn = psycopg2.connect("dbname=dndtoolkitdb user=olivia")
    cur = conn.cursor()

    # init_db(cur, conn)
    # init_tentacle_guy()
    # init_orc_guy()
    # print(get_character_stats("tentacle_guy"))


 






# Execute a command: this creates a new table
# cur.execute('CREATE TABLE books  (id serial PRIMARY KEY,'
#                                  'title varchar (150) NOT NULL,'
#                                  'author varchar (50) NOT NULL,'
#                                  'pages_num integer NOT NULL,'
#                                  'review text,'
#                                  'date_added date DEFAULT CURRENT_TIMESTAMP);'
#                                  )

