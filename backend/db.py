import sqlite3 as sq
import json as j

# create species table
def init_db():

    # TODO: create tables for remaining entities (sales, etc)

    with sq.connect("plants.db") as conn:
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

def insertPlant(plant):

    # assign values based on object keys to the respective variables
    genus = plant["genus"]
    species = plant["species"]
    status = plant["status"]
    qty = plant["qty"]
    wishlist = plant["wishlist"]
    
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
    with sq.connect("plants.db") as conn:
        c = conn.cursor()
        c.execute("""INSERT INTO plants (genus, species, status, qty, wishlist)
                    VALUES (:genus, :species, :status, :qty, :wishlist)""",

                    {'genus': genus, 'species': species, 'status' : status, 
                     'qty': qty, 'wishlist' : wishlist})


# return all logged plant species
def getPlants():
    with sq.connect("plants.db") as conn:
        conn.row_factory = sq.Row
        c = conn.execute("SELECT * FROM plants")
        rows = c.fetchall()
        return [dict(row) for row in rows]


# return all owned plants (non-wishlist)
def getOwnedPlants():
    with sq.connect("plants.db") as conn:
        conn.row_factory = sq.Row
        c = conn.execute("SELECT * FROM plants WHERE qty > 0")
        rows = c.fetchall()
        return [dict(row) for row in rows]


# return all wishlist plants
def getWishlistPlants():
    with sq.connect("plants.db") as conn:
        conn.row_factory = sq.Row
        c = conn.execute("SELECT * FROM plants WHERE wishlist = 1")
        rows = c.fetchall()
        return [dict(row) for row in rows]


# return a plant by ID (no front end use yet...)
def getByID(id):
    with sq.connect("plants.db") as conn:
        # create parser for row and fetch instance of a plant
        conn.row_factory = sq.Row
        c = conn.execute(
            'SELECT * FROM plants WHERE plantID = :id', {'id': id})
        plant = c.fetchone()
        return dict(plant) if plant else None


# TODO: get plants by genus
# TODO: get plants by status


# delete a plant by ID
def deletePlant(id):
    with sq.connect("plants.db") as conn:
        c = conn.cursor()
        c.execute("DELETE FROM plants WHERE plantID = :id", {'id' : id})
        conn.commit()


# update a plant (note: this requires you to pass the plant to front end 
# initially to pre-fill these fields to ensure the user sees OG values)
def updatePlant(plant):

    id = plant["plantID"]
    genus = plant["genus"]
    species = plant["species"]
    status = plant["status"]
    qty = plant["qty"]
    wishlist = plant["wishlist"]
    
    # if set to wishlist, reset qty + status
    if wishlist == 1:
        qty = 0
        status = 'wishlist'

    # Update all variables as needed
    with sq.connect("plants.db") as conn:
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

# TODO: make fields update-able in-table? May require a function to fetch the
# the attributes individually


