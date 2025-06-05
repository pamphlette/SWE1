import sqlite3 as sq        
from db import DATABASE     # make sure DB name is defined in db.py! 

def insertSale(data):
    """
    Inserts a new sale into the sales table.
    Expected keys in `data`: plantID, qty, price, unitID, date, note
    """
    plantID = data["plantID"]
    qty = data["qty"]
    price = data["price"]
    unitID = data["unitID"]
    date = data["date"]
    note = data.get("note", "")         # defaults to empty string if empty

    with sq.connect(DATABASE) as conn:
        c = conn.cursor()
        c.execute("""
            INSERT INTO sales (plantID, qty, price, unitID, date, note)
            VALUES (:plantID, :qty, :price, :unitID, :date, :note)""", 
        {
            'plantID': plantID,
            'qty': qty,
            'price': price,
            'unitID': unitID,
            'date': date,
            'note': note
        })
        conn.commit()

def getSales():
    """
    Fetch all sales records.
    :return: list of dictionaries
    """
    with sq.connect(DATABASE) as conn:
        conn.row_factory = sq.Row
        c = conn.execute("SELECT * FROM sales ORDER BY date DESC")
        rows = c.fetchall()
        return [dict(row) for row in rows]

def deleteSale(id):
    """
    Deletes a sale by its ID.
    :param id: saleID
    """
    with sq.connect(DATABASE) as conn:
        c = conn.cursor()
        c.execute("DELETE FROM sales WHERE saleID = :id", {'id': id})
        conn.commit()
    print(f"Deleted sale with ID {id}.")

def updateSale(data):
    """
    Updates an existing sale.
    Expects keys: saleID, plantID, qty, price, unitID, date, note
    """
    saleID = data["saleID"]
    plantID = data["plantID"]
    qty = data["qty"]
    price = data["price"]
    unitID = data["unitID"]
    date = data["date"]
    note = data.get("note", "")

    with sq.connect(DATABASE) as conn:
        c = conn.cursor()
        c.execute("""
            UPDATE sales SET
                plantID = :plantID,
                qty = :qty,
                price = :price,
                unitID = :unitID,
                date = :date,
                note = :note
            WHERE saleID = :saleID
        """, {
            'saleID': saleID,
            'plantID': plantID,
            'qty': qty,
            'price': price,
            'unitID': unitID,
            'date': date,
            'note': note
        })
        conn.commit()