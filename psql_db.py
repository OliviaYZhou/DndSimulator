import os
import psycopg2
import psycopg2.extras

conn = psycopg2.connect("dbname=dndtoolkitdb user=olivia")

# Open a cursor to perform database operations
cur = conn.cursor()

def init_db():
    # cur.execute('DROP TABLE IF EXISTS BASIC_CHARACTER CASCADE;')
    # cur.execute(
    #     '''CREATE TABLE BASIC_CHARACTER
    #     (ID              TEXT                PRIMARY KEY,
    #     NAME             TEXT,
    #     CHARACTER_TYPE   TEXT);''')  # player, npc, enemy


    # cur.execute('DROP TABLE IF EXISTS CHARACTER_STATS CASCADE;')
    # cur.execute(
    #     '''CREATE TABLE CHARACTER_STATS
    #     (
    #     CHARACTERID      TEXT        PRIMARY KEY   REFERENCES BASIC_CHARACTER, 
    #     LEVEL            INTEGER,
    #     HP               INTEGER,
    #     STR              INTEGER,
    #     DEX              INTEGER,
    #     CON              INTEGER,
    #     INT              INTEGER,
    #     WIS              INTEGER,
    #     CHA              INTEGER);''')


    # cur.execute('DROP TABLE IF EXISTS CUMULATIVE_STATS CASCADE;')
    # cur.execute(

    #     '''CREATE TABLE CUMULATIVE_STATS
    #     (
    #     CHARACTERID      TEXT   PRIMARY KEY REFERENCES BASIC_CHARACTER,
    #     GOLD             INTEGER,
    #     EXP              INTEGER);''')


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
    # cur.execute('DROP TABLE IF EXISTS INVENTORY_ITEMS CASCADE;')

    # cur.execute(
    #     '''CREATE TABLE INVENTORY_ITEMS
    #         (ITEM_NAME      TEXT   PRIMARY KEY,
    #         CHARACTERID     TEXT      NOT NULL REFERENCES BASIC_CHARACTER, 
    #         AMOUNT          INTEGER                NOT NULL,
    #         STATUSNAME      TEXT   REFERENCES STATUS_EFFECTS(NAME),
    #         DESCRIPTION     INTEGER)                    
    #         ;''')

    # cur.execute(
    # '''CREATE TABLE ITEMS
    #     (ITEMID         SERIAL   PRIMARY KEY,
    #     ITEMNAME        TEXT                   NOT NULL,        
    #     DESCRIPTION     INTEGER,
    #     EFFECTID        INTEGER)                    
    #     ;''')


    # cur.execute('DROP TABLE IF EXISTS SKILLS;')

    # cur.execute(
    #     '''CREATE TABLE SKILLS
    #         (SKILLID       SERIAL   PRIMARY KEY,
    #         NAME           TEXT                   NOT NULL,        
    #         LEVEL          TEXT                   NOT NULL,
    #         BASE           INT,
    #         MAXROLL        INT,
    #         DESCRIPTION    INTEGER)                    
    #         ;''')

# Execute a command: this creates a new table
# cur.execute('CREATE TABLE books  (id serial PRIMARY KEY,'
#                                  'title varchar (150) NOT NULL,'
#                                  'author varchar (50) NOT NULL,'
#                                  'pages_num integer NOT NULL,'
#                                  'review text,'
#                                  'date_added date DEFAULT CURRENT_TIMESTAMP);'
#                                  )


def add_character(character_id, name, character_type):
    cur.execute('INSERT INTO BASIC_CHARACTER (ID, NAME, CHARACTER_TYPE)'
            'VALUES (%s, %s, %s)',(character_id, name,character_type))

def add_character_stats(character_id, stats, level):
    if type(stats) == str:
        list_stats = stats.split(" ")
        cur.execute('INSERT INTO CHARACTER_STATS (CHARACTERID, LEVEL, HP, STR, DEX, CON, INT, WIS, CHA)'
        'VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s)', (character_id, level, list_stats[0], list_stats[1],
        list_stats[2], list_stats[3], list_stats[4], list_stats[5], list_stats[6]))

def add_status_effect(character_id, stats, effect_name , description='', duration=1):
    if type(stats) == str:
        list_stats = stats.split(" ")
        cur.execute('INSERT INTO STATUS_EFFECTS (NAME, CHARACTERID, HP, STR, DEX, CON, INT, WIS, CHA, DESCRIPTION, DURATION, DURATION_REMAINING)'
        'VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s)', (effect_name, character_id, list_stats[0], list_stats[1],
        list_stats[2], list_stats[3], list_stats[4], list_stats[5], list_stats[6], description, duration, duration))

def get_all_characters():
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
    # cursor = conn.cursor(cursor_factory = psycopg2.extras.RealDictCursor)
    q1 = '''
        SELECT SUM(HP), SUM(STR), SUM(DEX), SUM(CON), SUM(INT), SUM(WIS), SUM(CHA)
        FROM STATUS_EFFECTS WHERE CHARACTERID=(%s);'''

    cur.execute(q1, (charid,))
    status_effects = cur.fetchone()
    print(status_effects)

    q2 = '''
    SELECT HP, STR, DEX, CON, INT, WIS, CHA FROM CHARACTER_STATS WHERE CHARACTERID=(%s);
    '''
    cur.execute(q2, (charid,))
    max_stats = cur.fetchone()
    print(max_stats)

    current_stats = [max_stats[i] + status_effects[i] for i in range(7)]

    
    "[hp: 40/100, str: 19 (20-1), etc"
    return {"status_effects": status_effects, "max_stats":max_stats, "current_stats": current_stats}


def get_player_stats(charid):
    stats_dict = get_character_stats(charid)
    q1 = '''
    SELECT GOLD, EXP
    FROM CUMULATIVE_STATS WHERE CHARACTERID=ANY(%s);'''

    cur.execute(q1, (charid,))
    cumulative_stats = cur.fetchall()

    stats_dict["cumulative_stats"] = cumulative_stats

    return stats_dict
  
        # SELECT HP+MHP, STR+MSTR, DEX+MDEX, CON+MCON, INT+MINT, WIS+MWIS, CHA+MCHA 
        # FROM CHARACTER_STATS, MSTATS
        # WHERE CHARACTER_STATS.CHARACTERID = {charid};

        # SELECT SUM(HP) AS MHP, SUM(STR) AS MSTR, SUM(DEX) AS MDEX, SUM(CON) AS MCON, SUM(INT) AS MINT, SUM(WIS) AS MWIS, SUM(CHA) AS MCHA
        # FROM STATUS_EFFECTS WHERE CHARACTERID={CHARID};'''
def get_status_effects(stat, charid):
    q1 = """SELECT (%s), DESCRIPTION, DURATION, DURATION_REMAINING FROM STATUS_EFFECTS WHERE CHARACTERID=ANY(%s) AND (%s) != 0"""
    cur.execute(q1, (stat, charid))
    status_effects = cur.fetchall()
    return status_effects


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
    init_db()
    # add_character("tester2", "olivia2", "ncp")
    # add_character_stats("tester2", "20 5 6 7 8 9 10", 1)
    add_status_effect("tester2", "0 0 0 0 -1 0 0", "Crushed Spirit", "From working in factory", 5)
    add_status_effect("tester2", "0 0 0 0 0 -5 0", "Tired", "Loss of sleep", 1)
    add_status_effect("tester2", "0 0 0 0 0 1 0", "Candy", "energizing candy", 1)
    conn.commit()
    get_all_characters()
    print(get_character_stats("tester2"))
    cur.close()
    conn.close()



