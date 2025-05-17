from flask import Flask, jsonify, request
import db

# start flask instance and DB
app = Flask(__name__)
db.init_db()

# route for fetching plant inventory from the back-end
@app.route('/api/greenhouse')
def greenhouse():

    data = db.getPlants()
    print(data)
    return jsonify(data)

# adding a new plant
@app.route('/api/add-plant', methods=['POST'])
def add_plant():
    data = request.get_json()
    db.editPlant(**data)
    return jsonify({"message": "Plant edited"}), 200

@app.route('/api/edit-plant', methods=['POST'])
def edit_plant():
    data = request.get_json()
    print("Edit request received:", data)  # 👈

    try:
        db.updatePlant(**data)
    except Exception as e:
        print("Error in updatePlant:", e)  # 👈
        return jsonify({"error": str(e)}), 500

    return jsonify({"message": "Plant updated"}), 200


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