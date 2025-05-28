import sqlite3 as sq
import json as j

# replace with your intended database name
DATABASE = "plants" + ".db"         

# Create + populate a DB with table(s)  
def init_db():
    """
    Creates connection to existing database (or creates a DB with given name
    if it does not) and creates given tables. TODO: not tested to see what 
    would happen if new add table statement is added after db already exists
    """
    # connect to DB and execute block of SQL code to create table 
    with sq.connect(DATABASE) as conn:
        cursor = conn.cursor()
        cursor.execute("""CREATE TABLE IF NOT EXISTS plants (
            plantID INTEGER PRIMARY KEY AUTOINCREMENT,
            genus TEXT,
            species TEXT,
            status TEXT,
            qty INTEGER NOT NULL,
            wishlist INTEGER NOT NULL
        );""")
        conn.commit()

# insert object into DB from JSON obj, replace attributes as needed
def insertPlant(data):
    """
    Inserts the given object into the DB based on attribute + value. Assumes 
    that JSON object keys are of the same name as the attributes in the table.

    :param data:    JSON object with appropriate DB object attributes
                    (note: does not need ID # if int is primary key in DB)
    """
    # assign values based on object keys to the respective variables
    genus = data["genus"]
    species = data["species"]
    status = data["status"]
    qty = data["qty"]
    wishlist = data["wishlist"]
    
    # process any values that aren't already handled by the front end...
    if status == '':
        status = "unknown"
    if qty == 0:
        qty = 1

    #if the plant is toggled as a wishlist item, then no qty + status
    if wishlist == 1:
        qty = 0
        status = 'wishlist'

    # now insert values into the DB based on previously defined columns
    with sq.connect(DATABASE) as conn:
        c = conn.cursor()

        # make sure that the values inserted use :placeholder format
        c.execute("""INSERT INTO plants (genus, species, status, qty, wishlist)
                    VALUES (:genus, :species, :status, :qty, :wishlist)""",

                    {'genus': genus, 'species': species, 'status' : status, 
                     'qty': qty, 'wishlist' : wishlist})

# return all litems in table, replace table names as needed
def getPlants():
    """Fetch all rows from the table and return them as a list of dicts
    
    :SQL: "SELECT * FROM plants" """
    with sq.connect(DATABASE) as conn:
        conn.row_factory = sq.Row
        c = conn.execute("SELECT * FROM plants")
        rows = c.fetchall()
        return [dict(row) for row in rows]  


# return a plant by ID (no front end use yet...)
def getByID(id):
    """Fetches a specific plant by ID and returns it as a dict

    :SQL: 'SELECT * FROM plants WHERE plantID = :id' """
    with sq.connect(DATABASE) as conn:
        # create parser for row and fetch instance of a plant
        conn.row_factory = sq.Row
        c = conn.execute(
            'SELECT * FROM plants WHERE plantID = :id', {'id': id})
        plant = c.fetchone()
        return dict(plant) if plant else None


# delete a plant by ID
def deletePlant(id):
    """Deletes a specific row by ID

    :SQL: 'SELECT * FROM plants WHERE plantID = :id' """
    with sq.connect(DATABASE) as conn:
        c = conn.cursor()
        c.execute("DELETE FROM plants WHERE plantID = :id", {'id' : id})
        conn.commit()
    
    print(f"deleted row with id {id} in table (in DB)")


# update a plant (note: this requires you to pass the plant to front end 
# initially to pre-fill these fields & ensure the user sees OG values)
def updatePlant(data):
    """ Updates a DB item on any variables changed in the front end. Assumes 
    that the given JSON object has all of the needed keys.

    :param:     JSON object with appropriate DB object attributes
    """

    id = data["plantID"]
    genus = data["genus"]
    species = data["species"]
    status = data["status"]
    qty = data["qty"]
    wishlist = data["wishlist"]
    
    # if set to wishlist, reset qty + status
    if wishlist == 1:
        qty = 0
        status = 'wishlist'

    # Update all variables as needed
    with sq.connect(DATABASE) as conn:
        c = conn.cursor()
        c.execute("""UPDATE plants SET 
                  genus = :genus, 
                  species = :species, 
                  status = :status, 
                  qty = :qty, 
                  wishlist = :wishlist
                  WHERE plantID = :plantID
                  """, {
                      'genus': genus, 
                      'species': species, 
                      'status' : status, 
                      'qty': qty, 
                      'wishlist' : wishlist,
                      'plantID' : id})
        conn.commit()
