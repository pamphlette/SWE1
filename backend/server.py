from flask import Flask, jsonify, request
import db
from routes.plantRoutes import plantBP
from routes.expenseRoutes import expensesBP
from routes.saleRoutes import salesBP

# open terminal in the backend folder and run it 
# # flask --app server run -p 5000

# start flask instance and DB (or create one if it does not exist)
app = Flask(__name__)
db.initDB()
# db.checkDB()          # check all tables      
# db.checkDetail()      # check all tables + columns

# Register blueprints
app.register_blueprint(plantBP)
app.register_blueprint(expensesBP)
app.register_blueprint(salesBP)

# Running app
if __name__ == '__main__':
    app.run(debug=True)