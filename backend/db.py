import sqlite3

# create species table
def init_db():
    with sqlite3.connect("plants.db") as conn:
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

# insert a new plant species into the db using provided values
def insertPlant(genus = None, species = None, status = 'growing',
                qty = 1, wishlist = 0, ):
    
    # set to default values for table if no values are entered for these
    if status is None:
        status = "unknown"
    if qty is None:
        qty = 1
    if wishlist is None:
        wishlist = 0

    #if the plant is toggled as a wishlist item, then no qty + status
    if wishlist == 1:
        qty = 0
        status = 'wishlist'

    with sqlite3.connect("plants.db") as conn:
        c = conn.cursor()
        c.execute("""INSERT INTO plants (genus, species, status, qty, wishlist)
                  VALUES (:genus, :species, :status, :qty, :wishlist)""",
                    {'genus': genus, 'species': species, 'status' : status, 'qty': qty, 'wishlist' : wishlist})

# return all logged plant species
def getPlants():
    with sqlite3.connect("plants.db") as conn:
        conn.row_factory = sqlite3.Row
        cursor = conn.execute("SELECT * FROM plants")
        rows = cursor.fetchall()
        return [dict(row) for row in rows]

# return all owned plants (non-wishlist)
def getOwnedPlants():
    with sqlite3.connect("plants.db") as conn:
        c = conn.cursor()
        c.execute("SELECT * FROM plants WHERE wishlist = 0")
        return c.fetchall()

# return all wishlist plants
def getWishlistPlants():
    with sqlite3.connect("plants") as conn:
        c = conn.cursor()
        c.execute("SELECT * FROM plants WHERE wishlist = 1")
        return c.fetchall()

def getByID(id):
    with sqlite3.connect("plants.db") as conn:
        c = conn.cursor()
        # create parser for row and fetch instance of a plant
        conn.row_factory = sqlite3.Row
        c = conn.execute(
            'SELECT * FROM plants WHERE plantID = :id', {'id': id})
        plant = c.fetchone()
        return dict(plant) if plant else None
    
# TODO: get plants by genus
# TODO: get plants by status 
    
# delete a plant 
def deletePlant(id):
    with sqlite3.connect("plants.db") as conn:
        c = conn.cursor()
        c.execute("DELETE FROM plants WHERE plantID = :id", {'id' : id})
        conn.commit()

# update a plant
def updatePlant(plantID, genus = None, species = None, status = None,
                qty = None, wishlist = None):
    
    # if set to wishlist, reset qty + status
    if wishlist == 1:
        qty = 0
        status = 'wishlist'

    # fetch existing plant variables
    plant = getByID(plantID)
    if not plant:
        raise ValueError(f"No plant found with ID {plantID}")
    
    # determine if any variables changed
    if genus is not None:
        plant['genus'] = genus 
    if species is not None:
        plant['species'] = species 
    if status is not None:
        plant['status'] = status 
    if qty is not None:
        plant['qty'] = qty 
    if wishlist is not None:
        plant['wishlist'] = wishlist 

    # Upldate all variables
    with sqlite3.connect("plants.db") as conn:
        c = conn.cursor()
        c.execute("""UPDATE plants SET 
                  genus = :genus, 
                  species = :species, 
                  status = :status, 
                  qty = :qty, 
                  wishlist = :wishlist
                  WHERE plantID = :id
                  """, {
                      'genus': plant['genus'], 
                      'species': plant['species'], 
                      'status' : plant['status'], 
                      'qty': plant['qty'], 
                      'wishlist' : plant['wishlist'], 
                      'id' : plant['plantID']})
        conn.commit()



