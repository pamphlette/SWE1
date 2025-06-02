from flask import Flask, jsonify, request
import db

# open terminal in the backend folder and run it 
# # flask --app server run -p 5000

# TODO: add routes for sales/expenses/analytics

# start flask instance and DB (or create one if it does not exist)
app = Flask(__name__)
db.init_db()

# fetch entire plant inventory as JSON dicts
@app.route('/api/greenhouse')
def greenhouse():
    """Queries DB for a list of all DB objects and returns them to the frontend

    :return:    List of JSON dictionaries"""

    data = db.getPlants()
    # for x in data: print(x)     # verify return from the function

    return jsonify(data)        # return the plants


# fetch all plants with QTY > 0 as a bunch of JSON dicts
@app.route('/api/owned-plants')
def ownedPlants():
    """Queries DB for a list with dicts of DB objects and returns to frontend

    :return:    List of JSON dictionaries"""

    data = db.getOwnedPlants()
    # for x in data: print(x)     # verify return from the function

    print("owned plants: ", [plant for plant in data])
    return jsonify(data)          # return the plants


# fetch all wishlist plants as a bunch of JSON dicts
@app.route('/api/wishlist-plants')
def wishPlants():
    """Queries DB for a list with dicts of DB objects and returns to frontend

    :return:    List of JSON dictionaries"""

    data = db.getWishlistPlants()
    # for x in data: print(x)     # to verify return from the function

    if data: 
        return jsonify(data) 
    else: 
        print("Could not return data")


# Add new plant from JSON input
@app.route('/api/add-plant', methods=['POST'])
def add_plant():
    """Takes object data from front end to pass it to the DB for insertion, 
    returns a JSON dict with the inserted object data if successful"""

    data = request.get_json()
    print("Add request with this data: ", data) # check input
    
    try:
        db.insertPlant(data)
    except Exception as e:
        print("Error adding a new entry : ", e) # print exception
        return jsonify({"error": str(e)}), 500  # return exception to front end

    return jsonify({"inserted plant" : data}), 200       # return original data + status


# Update plant on all variables
@app.route('/api/edit-plant', methods=['POST'])
def edit_plant():
    """Takes object data from front end to pass it to the DB for updating, 
    returns a JSON dict with the updated object data if successful"""
        
    data = request.get_json()
    print("Edit request with this data: ", data)# check input

    try:
        db.updatePlant(data)
    except Exception as e:
        print("Error updating plant:", e)       # print exception
        return jsonify({"error": str(e)}), 500  # return exception to front end

    return jsonify({"updated plant" : data}), 200


# delete a given plant
@app.route('/api/delete-plant', methods=['POST'])
def delPlant():
    """Takes object ID from front end to pass it to the DB for deletion, 
    returns a JSON string with the deleted row ID if successful"""

    data = request.get_json()
    id = data.get('id')

    print("Received delete request with data:", data)

    # post warning if the id is nonexistent
    if id is None:
        return jsonify({"error": "No ID provided"}), 400

    db.deletePlant(id)
    return jsonify({"message": "Plant deleted", "id": id}), 200
    

# Running app
if __name__ == '__main__':
    app.run(debug=True)