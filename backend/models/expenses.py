import sqlite3 as sq        
from db import DATABASE     # make sure DB name is defined in db.py! 

def insertExpense(data):
    """
    Inserts a new expense into the expenses table.
    Expected keys in `data`: category, plantID (optional), qty, price, date, note
    """
    categoryID = data["categoryID"]
    qty = data["qty"]
    price = data["price"]
    date = data["date"]
    note = data.get("note", "")
    plantID = data.get("plantID")  # Optional

    with sq.connect(DATABASE) as conn:
        c = conn.cursor()
        c.execute("""
            INSERT INTO expenses (category, plantID, qty, price, date, note)
            VALUES (:category, :plantID, :qty, :price, :date, :note)
        """, {
            'category': categoryID,
            'plantID': plantID,
            'qty': qty,
            'price': price,
            'date': date,
            'note': note
        })
        conn.commit()

def getExpense():
    """
    Fetches all expenses from the database and joins category and plant info.
    Returns a list of dictionaries.
    """
    with sq.connect(DATABASE) as conn:
        conn.row_factory = sq.Row
        c = conn.execute("""
            SELECT 
                expenses.expenseID, 
                expenses.qty, 
                expenses.price,
                expenses.date,
                expenses.note,
                
                expenseCategories.category AS categoryName,
                
                plants.genus,
                plants.species
            FROM expenses
            LEFT JOIN expenseCategories 
                ON expenses.categoryID = expenseCategories.categoryID
            LEFT JOIN plants 
                ON expenses.plantID = plants.plantID
        """)
        rows = c.fetchall()
        return [dict(row) for row in rows]

def deleteExpense(id):
    """
    Deletes an expense by its ID.
    :param id: expenseID
    """
    with sq.connect(DATABASE) as conn:
        c = conn.cursor()
        c.execute("DELETE FROM expenses WHERE expenseID = :id", {'id': id})
        conn.commit()
    print(f"Deleted expense with ID {id}.")

def updateExpense(data):
    """
    Updates an existing expense.
    Expected keys: expenseID, category, plantID (optional), qty, price, date, note
    """
    expenseID = data["expenseID"]
    categoryID = data["categoryID"]
    qty = data["qty"]
    price = data["price"]
    date = data["date"]
    note = data.get("note", "")
    plantID = data.get("plantID")  # Optional

    with sq.connect(DATABASE) as conn:
        c = conn.cursor()
        c.execute("""
            UPDATE expenses SET
                category = :categoryID,
                plantID = :plantID,
                qty = :qty,
                price = :price,
                date = :date,
                note = :note
            WHERE expenseID = :expenseID
        """, {
            'expenseID': expenseID,
            'category': categoryID,
            'plantID': plantID,
            'qty': qty,
            'price': price,
            'date': date,
            'note': note
        })
        conn.commit()