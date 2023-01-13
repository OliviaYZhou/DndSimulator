def create_table_BASIC_CHARACTER(cur):
    cur.execute('DROP TABLE IF EXISTS BASIC_CHARACTER CASCADE;')
    cur.execute(
        '''CREATE TABLE BASIC_CHARACTER
        (ID              TEXT                PRIMARY KEY,
        NAME             TEXT,
        CHARACTER_TYPE   TEXT);''')  # player, npc, enemy

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

def create_table_CUMULATIVE_STATS(cur):
    cur.execute('DROP TABLE IF EXISTS CUMULATIVE_STATS CASCADE;')
    cur.execute(

        '''CREATE TABLE CUMULATIVE_STATS
        (
        CHARACTERID      TEXT   PRIMARY KEY REFERENCES BASIC_CHARACTER,
        GOLD             INTEGER,
        EXP              INTEGER);''')

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

def create_table_INVENTORY_ITEMS(cur):
    cur.execute('DROP TABLE IF EXISTS INVENTORY_ITEMS CASCADE;')

    cur.execute(
        '''CREATE TABLE INVENTORY_ITEMS
            (ITEM_NAME      TEXT   PRIMARY KEY,
            CHARACTERID     TEXT      NOT NULL REFERENCES BASIC_CHARACTER, 
            AMOUNT          INTEGER                NOT NULL,
            STATUSNAME      TEXT   REFERENCES STATUS_EFFECTS(NAME),
            DESCRIPTION     INTEGER)                    
            ;''')

def create_table_ITEMS(cur):
    cur.execute('DROP TABLE IF EXISTS ITEMS CASCADE;')
    cur.execute(
    '''CREATE TABLE ITEMS
        (ITEMID         SERIAL   PRIMARY KEY,
        ITEMNAME        TEXT                   NOT NULL,        
        DESCRIPTION     INTEGER,
        EFFECTID        INTEGER)                    
        ;''')
    
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

def save_db(conn):
    conn.commit()

def init_db(cur, conn):
    create_table_BASIC_CHARACTER(cur)
    create_table_CHARACTER_STATS(cur)
    create_table_CUMULATIVE_STATS(cur)
    create_table_STATUS_EFFECTS(cur)
    create_table_INVENTORY_ITEMS(cur)
    # create_table_ITEMS(cur)
    # create_table_SKILLS(cur)

    save_db(conn)







# Execute a command: this creates a new table
# cur.execute('CREATE TABLE books  (id serial PRIMARY KEY,'
#                                  'title varchar (150) NOT NULL,'
#                                  'author varchar (50) NOT NULL,'
#                                  'pages_num integer NOT NULL,'
#                                  'review text,'
#                                  'date_added date DEFAULT CURRENT_TIMESTAMP);'
#                                  )

