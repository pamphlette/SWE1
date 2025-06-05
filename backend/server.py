from flask import Flask, jsonify, request
import db
import sqlite3 as sq
from routes.plantRoutes import plantBP
from routes.expenseRoutes import expensesBP
from routes.saleRoutes import salesBP

# open terminal in the backend folder and run it 
# # flask --app server run -p 5000

# start flask instance and DB (or create one if it does not exist)
app = Flask(__name__)
db.initDB()
# db.insert()
# db.checkDB()          # check all tables      
# db.checkDetail()      # check all tables + columns
# db.clearDB()          # clear all values from DB

# Register blueprints
app.register_blueprint(plantBP)
app.register_blueprint(expensesBP)
app.register_blueprint(salesBP)

#one-off to get all support FKs for drop-downs
@app.route('/api/statuses')
def getStatuses():
    with sq.connect(db.DATABASE) as conn:
        conn.row_factory = sq.Row
        rows = conn.execute("SELECT * FROM statuses").fetchall()
        return jsonify([dict(row) for row in rows])

@app.route('/api/units')
def getUnits():
    with sq.connect(db.DATABASE) as conn:
        conn.row_factory = sq.Row
        rows = conn.execute("SELECT * FROM unitTypes").fetchall()
        return jsonify([dict(row) for row in rows])

@app.route('/api/categories')
def getCategories():
    with sq.connect(db.DATABASE) as conn:
        conn.row_factory = sq.Row
        rows = conn.execute("SELECT * FROM expenseCategories").fetchall()
        return jsonify([dict(row) for row in rows])

# Running app
if __name__ == '__main__':
    app.run(debug=True)