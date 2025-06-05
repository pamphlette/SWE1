from flask import Blueprint, jsonify, request
from models import expenses

expensesBP = Blueprint('expensesBP', __name__)

# GET: Fetch all expenses
@expensesBP.route('/api/expenses')
def getExpenses():
    """Fetches all expense records and returns as JSON"""
    try:
        data = expenses.getExpense()
        return jsonify(data)
    except Exception as e:
        print("Error fetching expenses:", e)
        return jsonify({"error": str(e)}), 500


# POST: Add a new expense
@expensesBP.route('/api/add-expense', methods=['POST'])
def addExpense():
    """Adds a new expense to the DB"""
    data = request.get_json()
    print("Add expense request data:", data)

    try:
        expenses.insertExpense(data)
        return jsonify({"inserted expense": data}), 200
    except Exception as e:
        print("Error inserting expense:", e)
        return jsonify({"error": str(e)}), 500


# POST: Edit an existing expense
@expensesBP.route('/api/edit-expense', methods=['POST'])
def editExpense():
    """Updates an existing expense in the DB"""
    data = request.get_json()
    print("Edit expense request data:", data)

    try:
        expenses.updateExpense(data)
        return jsonify({"updated expense": data}), 200
    except Exception as e:
        print("Error updating expense:", e)
        return jsonify({"error": str(e)}), 500


# POST: Delete an expense
@expensesBP.route('/api/delete-expense', methods=['POST'])
def delExpense():
    """Deletes an expense from the DB by ID"""
    data = request.get_json()
    expense_id = data.get('id')

    if expense_id is None:
        return jsonify({"error": "No expense ID provided"}), 400

    try:
        expenses.deleteExpense(expense_id)
        return jsonify({"message": "Expense deleted", "id": expense_id}), 200
    except Exception as e:
        print("Error deleting expense:", e)
        return jsonify({"error": str(e)}), 500