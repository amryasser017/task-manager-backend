from flask import Flask, jsonify, request
from flask_cors import CORS
from flask_jwt_extended import JWTManager, create_access_token, jwt_required, get_jwt_identity
import mysql.connector
import bcrypt

app = Flask(__name__)
CORS(app)

# JWT secret key — keep this secret in real apps!
app.config['JWT_SECRET_KEY'] = 'your-secret-key-123'
jwt = JWTManager(app)

def get_db():
    return mysql.connector.connect(
        host='tramway.proxy.rlwy.net',
        port=46060,
        user='root',
        password='AUmwfnhxljAMNZYZkDucUxXCkMxrOCeq',
        database='railway'
    )

# ── REGISTER ──
@app.route('/api/register', methods=['POST'])
def register():
    data = request.json
    username = data['username']
    email = data['email']
    password = data['password']

    # Hash the password
    hashed = bcrypt.hashpw(password.encode('utf-8'), bcrypt.gensalt())

    try:
        db = get_db()
        cursor = db.cursor()
        cursor.execute(
            'INSERT INTO users (username, email, password) VALUES (%s, %s, %s)',
            (username, email, hashed.decode('utf-8'))
        )
        db.commit()
        cursor.close()
        db.close()
        return jsonify({'message': 'User registered successfully'}), 201
    except Exception as e:
        return jsonify({'error': 'Username or email already exists'}), 400

# ── LOGIN ──
@app.route('/api/login', methods=['POST'])
def login():
    data = request.json
    email = data['email']
    password = data['password']

    db = get_db()
    cursor = db.cursor(dictionary=True)
    cursor.execute('SELECT * FROM users WHERE email = %s', (email,))
    user = cursor.fetchone()
    cursor.close()
    db.close()

    if not user:
        return jsonify({'error': 'User not found'}), 404

    # Check password against hash
    if bcrypt.checkpw(password.encode('utf-8'), user['password'].encode('utf-8')):
        token = create_access_token(identity=str(user['id']))
        return jsonify({'token': token, 'username': user['username']}), 200
    else:
        return jsonify({'error': 'Wrong password'}), 401

# ── GET tasks (protected) ──
@app.route('/api/tasks', methods=['GET'])
@jwt_required()
def get_tasks():
    user_id = get_jwt_identity()
    db = get_db()
    cursor = db.cursor(dictionary=True)
    cursor.execute('SELECT * FROM tasks WHERE user_id = %s', (user_id,))
    tasks = cursor.fetchall()
    cursor.close()
    db.close()
    return jsonify(tasks)

# ── CREATE task (protected) ──
@app.route('/api/tasks', methods=['POST'])
@jwt_required()
def create_task():
    user_id = get_jwt_identity()
    data = request.json
    db = get_db()
    cursor = db.cursor()
    cursor.execute(
        'INSERT INTO tasks (title, description, user_id) VALUES (%s, %s, %s)',
        (data['title'], data.get('description', ''), user_id)
    )
    db.commit()
    cursor.close()
    db.close()
    return jsonify({'message': 'Task created successfully'}), 201

# ── UPDATE task (protected) ──
@app.route('/api/tasks/<int:id>', methods=['PUT'])
@jwt_required()
def update_task(id):
    data = request.json
    db = get_db()
    cursor = db.cursor()
    cursor.execute(
        'UPDATE tasks SET status=%s WHERE id=%s',
        (data['status'], id)
    )
    db.commit()
    cursor.close()
    db.close()
    return jsonify({'message': 'Task updated successfully'})

# ── DELETE task (protected) ──
@app.route('/api/tasks/<int:id>', methods=['DELETE'])
@jwt_required()
def delete_task(id):
    db = get_db()
    cursor = db.cursor()
    cursor.execute('DELETE FROM tasks WHERE id=%s', (id,))
    db.commit()
    cursor.close()
    db.close()
    return jsonify({'message': 'Task deleted successfully'})

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=8080, debug=True)