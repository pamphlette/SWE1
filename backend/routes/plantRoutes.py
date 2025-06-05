from flask import Blueprint, jsonify, request
from models import plants

plantBP = Blueprint('plantBP', __name__)

@plantBP.route('/api/greenhouse')
def greenhouse():
    """Queries DB for a list of all DB objects and returns them to the frontend"""

    data = plants.getPlants()
    # for x in data: print(x)     # verify return from the function
    return jsonify(data)        # return the plants


@plantBP.route('/api/owned-plants')
def ownedPlants():
    """Queries DB for a list with dicts of DB objects and returns to frontend"""

    data = plants.getOwnedPlants()
    # for x in data: print(x)     # verify return from the function
    return jsonify(data)          # return the plants


# fetch all wishlist plants as a bunch of JSON dicts
@plantBP.route('/api/wishlist-plants')
def wishPlants():
    """Queries DB for a list with dicts of DB objects and returns to frontend"""

    data = plants.getWishlistPlants()
    # for x in data: print(x)     # to verify return from the function
    if data: 
        return jsonify(data) 
    else: 
        print("Could not return data")


# Add new plant from JSON input
@plantBP.route('/api/add-plant', methods=['POST'])
def add_plant():
    """Takes object data from front end to pass it to the DB for insertion, 
    returns a JSON dict with the inserted object data if successful"""

    data = request.get_json()
    print("Add request with this data: ", data) # check input
    
    try:
        plants.insertPlant(data)
        return jsonify({"inserted plant" : data}), 200
    except Exception as e:
        return jsonify({"error": str(e)}), 500  # return exception to front end


# Update plant on all variables
@plantBP.route('/api/edit-plant', methods=['POST'])
def edit_plant():
    """Takes object data from front end to pass it to the DB for updating, 
    returns a JSON dict with the updated object data if successful"""

    data = request.get_json()
    print("Edit request with this data: ", data)# check input

    try:
        plants.updatePlant(data)
        return jsonify({"updated plant" : data}), 200
    except Exception as e:
        return jsonify({"error": str(e)}), 500  # return exception to front end


# delete a given plant
@plantBP.route('/api/delete-plant', methods=['POST'])
def delPlant():
    """Delete a plant from DB given ID"""

    data = request.get_json()
    plant_id = data.get('id')   

    if plant_id is None:
        return jsonify({"error": "No ID provided"}), 400
    plants.deletePlant(plant_id)
    return jsonify({"message": "Plant deleted", "id": plant_id}), 200