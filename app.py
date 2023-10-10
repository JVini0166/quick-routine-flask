from flask import Flask, request, jsonify
import migrations
import repository
from flask_cors import CORS

app = Flask(__name__)
CORS(app, headers='Content-Type')

migrations.execute_migrations()
# migrations.delete_all_tables()

PREFIX = "/quick-routine"

print("As seguintes tabelas foram encontradas:" + str(repository.get_all_tables()))


# CREATE Operations ENDPOINT


@app.route(PREFIX + '/create_user', methods=["POST"])
def create_user_endpoint():
    data = request.json

    # Extract data
    username = data.get('username')
    password = data.get('password')
    email = data.get('email')

    # Validate required fields
    if not all([username, password, email]):
        return jsonify({"message": "Missing required fields"}), 400

    # Check if user exists
    if repository.user_exists(username, email):
        return jsonify({"message": "User already created"}), 409

    # Create user
    try:
        user_id = repository.create_user(username, password, email)
        return jsonify({"message": "User created successfully", "user_id": user_id}), 201
    except Exception as e:
        return jsonify({"message": f"Error creating user: {str(e)}"}), 500



@app.route(PREFIX + '/create_review_template', methods=["POST"])
def create_review_template_endpoint():
    data = request.json
    
    # Extraia os dados do request
    description = data.get('description')
    period = data.get('period')

    # Verifica se os campos obrigatórios estão presentes
    # Neste caso, eu estou assumindo que todos os campos são opcionais. 
    # Modifique conforme a sua necessidade.
    
    try:
        template_id = repository.create_review_template(description, period)
        return jsonify({"message": "Review template created successfully", "template_id": template_id}), 201
    except Exception as e:
        return jsonify({"error": str(e)}), 500


@app.route(PREFIX + '/create_task', methods=["POST"])
def create_task_endpoint():
    data = request.json
    
    # Extraia os dados do request
    name = data.get('name')
    description = data.get('description')
    frequency = data.get('frequency')
    start_date = data.get('start_date')
    target_date = data.get('target_date')
    user_id = data.get('user_id')

    # Verifica se os campos obrigatórios estão presentes
    if not all([name, user_id]):
        return jsonify({"error": "Missing required fields"}), 400

    try:
        task_id = repository.create_task(name, description, frequency, start_date, target_date, user_id)
        return jsonify({"message": "Task created successfully", "task_id": task_id}), 201
    except Exception as e:
        return jsonify({"error": str(e)}), 500


@app.route(PREFIX + '/create_review', methods=["POST"])
def create_review_endpoint():
    data = request.json
    
    # Extraia os dados do request
    review_template_id = data.get('review_template_id')
    review_date = data.get('review_date')

    # Verifica se os campos obrigatórios estão presentes
    if not all([review_template_id, review_date]):
        return jsonify({"error": "Missing required fields"}), 400

    try:
        review_id = repository.create_review(review_template_id, review_date)
        return jsonify({"message": "Review created successfully", "review_id": review_id}), 201
    except Exception as e:
        return jsonify({"error": str(e)}), 500


@app.route(PREFIX + '/create_pomodoro', methods=["POST"])
def create_pomodoro_endpoint():
    data = request.json
    
    # Extraia os dados do request
    duration = data.get('duration')
    date = data.get('date')
    quantity = data.get('quantity')
    user_id = data.get('user_id')

    # Verifica se os campos obrigatórios estão presentes
    if not all([duration, date, quantity, user_id]):
        return jsonify({"error": "Missing required fields"}), 400

    try:
        pomodoro_id = repository.create_pomodoro(duration, date, quantity, user_id)
        return jsonify({"message": "Pomodoro created successfully", "pomodoro_id": pomodoro_id}), 201
    except Exception as e:
        return jsonify({"error": str(e)}), 500


# CREATE Operations ENDPOINT END



@app.route(PREFIX + '/get_all_tables')
def get_all_tables():
    return repository.get_all_tables()


@app.route(PREFIX + '/')
def hello_world():
    return 'Hello, World!'