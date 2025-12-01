from flask import Flask, request, jsonify
from flask_cors import CORS
import user_db  # Imports your database logic

app = Flask(__name__)
CORS(app)  # Enables frontend connection

# --- INITIALIZE DATABASE ---
try:
    user_db.create_table()
    print("Database connected and tables initialized.")
except Exception as e:
    print(f"Error initializing database: {e}")

# --- HOME ROUTE ---
@app.route('/')
def home():
    return "BudBuddy Server is Running!"

# --- AUTH ROUTES ---

@app.route('/register', methods=['POST'])
def register():
    data = request.get_json()
    try:
        # Now passing Email as the middle argument
        user_db.insert_user(data['username'], data['email'], data['password'])
        return jsonify({"success": True, "message": "User registered successfully"}), 201
    except Exception as e:
        print(f"Register Error: {e}")
        return jsonify({"success": False, "message": "Username or Email already exists"}), 400

@app.route('/login', methods=['POST'])
def login():
    data = request.get_json()
    try:
        if user_db.validate_user(data['username'], data['password']):
            return jsonify({"success": True, "token": data['username']}), 200
        else:
            return jsonify({"success": False, "message": "Invalid credentials"}), 401
    except Exception as e:
        return jsonify({"success": False, "message": f"Server error: {str(e)}"}), 500

@app.route('/reset_password', methods=['PUT'])
def reset_password():
    data = request.get_json()
    username = data.get('username')
    email = data.get('email')
    new_password = data.get('new_password')

    if not username or not email or not new_password:
        return jsonify({"success": False, "message": "Missing fields"}), 400

    try:
        # Requires both Username and Email to match
        if user_db.update_password(username, email, new_password):
            return jsonify({"success": True, "message": "Password updated"}), 200
        else:
            return jsonify({"success": False, "message": "Username and Email do not match"}), 404
    except Exception as e:
        return jsonify({"success": False, "message": str(e)}), 500

# --- GOAL ROUTES ---

@app.route('/goals', methods=['GET'])
def fetch_goals():
    username = request.args.get('username')
    try:
        goals = user_db.get_goals(username)
        return jsonify(goals), 200
    except Exception as e:
        return jsonify({"error": str(e)}), 500

@app.route('/add_goal', methods=['POST'])
def new_goal():
    data = request.get_json()
    try:
        user_db.add_goal(
            data['username'],
            data['title'],
            data['target'],
            data['current'],
            data['date']
        )
        return jsonify({"success": True}), 201
    except Exception as e:
        return jsonify({"error": str(e)}), 500

@app.route('/edit_goal', methods=['PUT'])
def edit_goal():
    data = request.get_json()
    try:
        user_db.update_goal(
            data['id'],
            data['title'],
            data['target'],
            data['current'],
            data['date']
        )
        return jsonify({"success": True}), 200
    except Exception as e:
        return jsonify({"error": str(e)}), 500

@app.route('/stats', methods=['GET'])
def get_stats():
    username = request.args.get('username')
    try:
        stats = user_db.get_dashboard_stats(username)
        return jsonify(stats), 200
    except Exception as e:
        return jsonify({"error": str(e)}), 500

# --- BUDGET & EXPENSE ROUTES ---

@app.route('/budgets', methods=['GET'])
def fetch_budgets():
    username = request.args.get('username')
    try:
        budgets = user_db.get_budgets_with_spending(username)
        return jsonify(budgets), 200
    except Exception as e:
        return jsonify({"error": str(e)}), 500

@app.route('/add_budget', methods=['POST'])
def new_budget():
    data = request.get_json()
    try:
        user_db.add_budget(data['username'], data['category'], data['amount'])
        return jsonify({"success": True}), 201
    except Exception as e:
        return jsonify({"error": str(e)}), 500

@app.route('/delete_budget', methods=['DELETE'])
def remove_budget():
    budget_id = request.args.get('id')
    try:
        user_db.delete_budget(budget_id)
        return jsonify({"success": True}), 200
    except Exception as e:
        return jsonify({"error": str(e)}), 500

@app.route('/add_expense', methods=['POST'])
def new_expense():
    data = request.get_json()
    try:
        user_db.add_expense(
            data['budget_id'],
            data['description'],
            data['amount'],
            data['date']
        )
        return jsonify({"success": True}), 201
    except Exception as e:
        return jsonify({"error": str(e)}), 500

if __name__ == '__main__':
    app.run(debug=True, port=5000)
