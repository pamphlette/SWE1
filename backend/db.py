import sqlite3 as sq

# replace with your intended database name
DATABASE = "plants" + ".db"         

# Create + populate a DB with table(s) using an SQL schema file
def initDB():
    """
    Creates connection to existing database (or creates a DB with given name
    if it does not) and creates given tables.
    """
    # connect to DB and execute block of SQL code to create table 
    with sq.connect(DATABASE) as conn:
        with open("schema.sql", "r") as schema:
            conn.executescript(schema.read())
            conn.commit()

def checkDB():
    """
    Prints a list of all tables that exist in the DB
    """
    with sq.connect(DATABASE) as conn:
        cur = conn.cursor()
        cur.execute("SELECT name FROM sqlite_master WHERE type='table';")
        tables = cur.fetchall()

        #print results
        print("TABLES:")
        for t in tables:
            print(t)
    
def checkDetail():
    """
    Prints all tables and their columns + PK and other constraints
    """
    allTables = []      # output list
    
    with sq.connect(DATABASE) as conn:
        # grab a list of tables first
        cur = conn.cursor()
        cur.execute("SELECT name FROM sqlite_master WHERE type='table';")
        tables = [row[0] for row in cur.fetchall()] 

        #then add them all to a return list
        for table in tables:
            cur.execute(f"PRAGMA table_info({table});")
            columns = cur.fetchall()
            allTables.append((table,columns))
    
    for table, columns in allTables:
        if table != "sqlite_sequence":
            print(f"\nTABLE: {table}")
            for col in columns:
                print(f"  {col[1]} ({col[2]})"          # col name + type
                f"{' NOT NULL' if col[3] else ''}"      # not null req 
                f"{' PRIMARY KEY' if col[5] else ''}")  # PK indicator
        