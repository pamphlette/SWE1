from flask import Blueprint, jsonify, request
from models import sales

salesBP = Blueprint('salesBP', __name__)

@salesBP.route('/api/sales')
def getSales():
    """Fetches all sale entries and returns as JSON list"""
    data = sales.getSales()
    return jsonify(data)

@salesBP.route('/api/add-sale', methods=['POST'])
def addSale():
    """Adds a new sale to the DB"""
    data = request.get_json()
    print("Add sale request data:", data)

    try:
        sales.insertSale(data)
        return jsonify({"inserted sale": data}), 200
    except Exception as e:
        print("Error inserting sale:", e)
        return jsonify({"error": str(e)}), 500

@salesBP.route('/api/edit-sale', methods=['POST'])
def editSale():
    """Updates an existing sale in the DB"""
    data = request.get_json()
    print("Edit sale request data:", data)

    try:
        sales.updateSale(data)
        return jsonify({"updated sale": data}), 200
    except Exception as e:
        print("Error updating sale:", e)
        return jsonify({"error": str(e)}), 500

@salesBP.route('/api/delete-sale', methods=['POST'])
def delSale():
    """Deletes a sale from the DB by ID"""
    data = request.get_json()
    sale_id = data.get('id')

    if sale_id is None:
        return jsonify({"error": "No sale ID provided"}), 400

    try:
        sales.deleteSale(sale_id)
        return jsonify({"message": "Sale deleted", "id": sale_id}), 200
    except Exception as e:
        print("Error deleting sale:", e)
        return jsonify({"error": str(e)}), 500