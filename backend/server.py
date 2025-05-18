from flask import Flask, jsonify, request
import db

# start flask instance and your DB
app = Flask(__name__)
db.init_db()

# fetch entire plant inventory as a bunch of JSON dicts
@app.route('/api/greenhouse')
def greenhouse():

    data = db.getPlants()
    # for x in data: print(x)     # verify return from the function

    return jsonify(data)        # return the plants

# fetch all plants with QTY > 0 as a bunch of JSON dicts
@app.route('/api/owned-plants')
def ownedPlants():

    data = db.getOwnedPlants()
    # for x in data: print(x)     # verify return from the function

    print("owned plants: ", [plant for plant in data])
    return jsonify(data)        # return the plants

# fetch all wishlist plants as a bunch of JSON dicts
@app.route('/api/wishlist-plants')
def wishPlants():

    data = db.getWishlistPlants()
    # for x in data: print(x)     # verify return from the function

    print("wishlist plants: ", [plant for plant in data])
    return jsonify(data)        # return the plants

# Add new plant from JSON input
@app.route('/api/add-plant', methods=['POST'])
def add_plant():

    data = request.get_json()
    print("Add request with this data: ", data) # check input
    
    try:
        db.insertPlant(data)
    except Exception as e:
        print("Error adding a new entry : ", e) # print exception
        return jsonify({"error": str(e)}), 500  # return exception to front end

    return jsonify({"plant" : data}), 200       # return original data + status

# Update plant on all variables
@app.route('/api/edit-plant', methods=['POST'])
def edit_plant():

    data = request.get_json()
    print("Edit request with this data: ", data)# check input

    try:
        db.updatePlant(data)
    except Exception as e:
        print("Error updating plant:", e)       # print exception
        return jsonify({"error": str(e)}), 500  # return exception to front end

    return jsonify({"plant" : data}), 200

# delete a given plant
@app.route('/api/delete-plant', methods=['POST'])
def delPlant():

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