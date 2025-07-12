import psycopg2
import boto3
import json
from flask import Flask, jsonify, request, abort
from flask_cors import CORS
from psycopg2.extras import RealDictCursor
from botocore.exceptions import ClientError

ENDPOINT = "test-api-database.csj2q2ssegfh.us-east-1.rds.amazonaws.com"
PORT = "5432"
DBNAME = "hello_world_db"

app = Flask(__name__)
CORS(app)

@app.route('/hello')
def hello():
    return jsonify(message="Hello, world!")

def get_conn():
    secret_name = "rds!db-335613cb-f3af-460f-93e9-2b452885ccf1"
    region_name = "us-east-1"

    # Create a Secrets Manager client
    sm_client = boto3.client(
        service_name='secretsmanager',
        region_name=region_name
    )

    try:
        response = sm_client.get_secret_value(
            SecretId=secret_name
        )
    except ClientError as e:
        # For a list of exceptions thrown, see
        # https://docs.aws.amazon.com/secretsmanager/latest/apireference/API_GetSecretValue.html
        raise e

    secret = json.loads(response['SecretString'])

    rds_client = boto3.client(
        service_name='rds',
        region_name=region_name
    )

    try:
        conn = psycopg2.connect(
            dbname=DBNAME,
            user=secret['username'],
            password=secret['password'],
            host=ENDPOINT,
            port=PORT,
            cursor_factory=RealDictCursor
        )
    except Exception as e:
        raise e

    return conn

# Initialize users table
@app.before_request
def init_db():
    with get_conn() as conn:
        with conn.cursor() as cur:
            cur.execute("""
                CREATE TABLE IF NOT EXISTS users (
                  id SERIAL PRIMARY KEY,
                  name TEXT NOT NULL,
                  email TEXT NOT NULL UNIQUE
                );
            """)
            conn.commit()

# List users
@app.route('/users', methods=['GET'])
def list_users():
    with get_conn() as conn:
        with conn.cursor() as cur:
            cur.execute("SELECT * FROM users ORDER BY id;")
            return jsonify(cur.fetchall())

# Create user
@app.route('/users', methods=['POST'])
def create_user():
    data = request.get_json() or {}
    name, email = data.get('name'), data.get('email')
    if not name or not email:
        abort(400, "name and email required")
    with get_conn() as conn:
        with conn.cursor() as cur:
            cur.execute(
              "INSERT INTO users (name,email) VALUES (%s,%s) RETURNING *;",
              (name, email)
            )
            user = cur.fetchone()
            conn.commit()
            return jsonify(user), 201

# Update user
@app.route('/users/<int:user_id>', methods=['PUT'])
def update_user(user_id):
    data = request.get_json() or {}
    name, email = data.get('name'), data.get('email')
    with get_conn() as conn:
        with conn.cursor() as cur:
            cur.execute("SELECT * FROM users WHERE id=%s;", (user_id,))
            if not cur.fetchone():
                abort(404)
            cur.execute(
              "UPDATE users SET name=%s, email=%s WHERE id=%s RETURNING *;",
              (name, email, user_id)
            )
            user = cur.fetchone()
            conn.commit()
            return jsonify(user)

# Delete user
@app.route('/users/<int:user_id>', methods=['DELETE'])
def delete_user(user_id):
    with get_conn() as conn:
        with conn.cursor() as cur:
            cur.execute("DELETE FROM users WHERE id=%s RETURNING *;", (user_id,))
            user = cur.fetchone()
            conn.commit()
            if not user:
                abort(404)
            return jsonify(user)

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000)
