import os
import sqlite3

from flask import Flask, Response, g, jsonify, request
from flask_jwt_extended import (JWTManager, create_access_token,
                                get_jwt_identity, jwt_required)
from werkzeug.security import check_password_hash, generate_password_hash

# Initialize the Flask app
app = Flask(__name__)
# For simplicity, I am using a static secret key here.
app.config["JWT_SECRET_KEY"] = "my_secret_key"

# Initialize the JWTManager
jwt = JWTManager(app)

# Path to the SQLite database file
DATABASE = os.path.join(app.root_path, "cloud_clicker.db")


def get_db() -> sqlite3.Connection:
    """
    Connect to the SQLite database.

    Returns:
        sqlite3.Connection: The database connection object.
    """
    db = getattr(g, "_database", None)
    if db is None:
        db = g._database = sqlite3.connect(DATABASE)
    return db


@app.teardown_appcontext
def close_connection(exception) -> None:
    """Close the database connection at the end."""
    db = getattr(g, "_database", None)
    if db is not None:
        db.close()


def init_db() -> None:
    """Initialize the database with the required tables."""

    with app.app_context():
        db = get_db()
        cursor = db.cursor()

        # Create Clicks table
        # This table will store the total click count
        cursor.execute(
            """
            CREATE TABLE IF NOT EXISTS clicks (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                count INTEGER NOT NULL
            )
        """
        )

        # Create Users table
        # This table will store the user details - username and password
        cursor.execute(
            """
            CREATE TABLE IF NOT EXISTS users (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                username TEXT NOT NULL UNIQUE,
                password TEXT NOT NULL
            )
        """
        )

        # Create User Clicks table
        # This table will store the click count for each user
        cursor.execute(
            """
            CREATE TABLE IF NOT EXISTS user_clicks (
                user_id INTEGER NOT NULL,
                clicks INTEGER NOT NULL,
                FOREIGN KEY(user_id) REFERENCES users(id)
            )
        """
        )

        # Insert the initial click count if it doesn't exist
        cursor.execute("SELECT COUNT(*) FROM clicks")
        if cursor.fetchone()[0] == 0:
            cursor.execute("INSERT INTO clicks (count) VALUES (0)")

        db.commit()


# API endpoint to register a new user
@app.route("/api/register", methods=["POST"])
def register() -> Response:
    """
    Register a new user.

    Returns:
        JSON: A JSON object with a message indicating the success or failure of the registration.
    """
    data = request.get_json()
    username = data.get("username")
    password = data.get("password")
    hashed_password = generate_password_hash(password)

    db = get_db()
    cursor = db.cursor()
    try:
        cursor.execute(
            "INSERT INTO users (username, password) VALUES (?, ?)", (username, hashed_password)
        )
        db.commit()

    except sqlite3.IntegrityError:
        return jsonify({"msg": "Username already exists"}), 409

    return jsonify({"msg": "User registered successfully"}), 201


# API endpoint to login and get a token
@app.route("/api/login", methods=["POST"])
def login() -> Response:
    """
    Login and get an access token.

    Returns:
        JSON: A JSON object with the access token if the login is successful,
              otherwise a message indicating the failure.
    """
    data = request.get_json()
    username = data.get("username")
    password = data.get("password")

    db = get_db()
    cursor = db.cursor()
    cursor.execute("SELECT * FROM users WHERE username = ?", (username,))
    user = cursor.fetchone()

    print(user, generate_password_hash(password))  # Debugging
    if user and check_password_hash(user[2], password):
        access_token = create_access_token(identity={"user_id": user[0], "username": username})
        return jsonify(access_token=access_token)
    else:
        return jsonify({"msg": "Bad username or password"}), 401


# API endpoint to get the total click count
@app.route("/api/clicks", methods=["GET"])
def get_clicks() -> Response:
    """
    Get the total click count.

    Returns:
        JSON: A JSON object with the total click count.
    """
    db = get_db()
    cursor = db.cursor()
    cursor.execute("SELECT count FROM clicks WHERE id = 1")
    click_data = cursor.fetchone()
    return jsonify({"count": click_data[0]})


# API endpoint to get the user's click count
@app.route("/api/user_clicks", methods=["GET"])
@jwt_required()
def get_user_clicks() -> Response:
    """
    Get the user's click count.

    Requires:
        JWT token in the Authorization header.

    Returns:
        JSON: A JSON object with the user's click count.
    """
    identity = get_jwt_identity()
    user_id = identity["user_id"]

    db = get_db()
    cursor = db.cursor()
    cursor.execute("SELECT clicks FROM user_clicks WHERE user_id = ?", (user_id,))
    user_click_data = cursor.fetchone()

    if user_click_data:
        user_clicks = user_click_data[0]
    else:
        user_clicks = 0

    return jsonify({"user_clicks": user_clicks})


# API endpoint to increment the click count
@app.route("/api/clicks", methods=["POST"])
@jwt_required()
def increment_clicks() -> Response:
    """
    Increment the total click count and the user's click count.

    Requires:
        JWT token in the Authorization header.

    Returns:
        JSON: A JSON object with the updated total click count and the user's click count.
    """
    identity = get_jwt_identity()
    user_id = identity["user_id"]

    db = get_db()
    cursor = db.cursor()

    # Increment total clicks
    cursor.execute("SELECT count FROM clicks WHERE id = 1")
    click_data = cursor.fetchone()
    new_count = click_data[0] + 1
    cursor.execute("UPDATE clicks SET count = ? WHERE id = 1", (new_count,))

    # Increment user clicks
    cursor.execute("SELECT clicks FROM user_clicks WHERE user_id = ?", (user_id,))
    user_click_data = cursor.fetchone()
    if user_click_data:
        new_user_count = user_click_data[0] + 1
        cursor.execute(
            "UPDATE user_clicks SET clicks = ? WHERE user_id = ?", (new_user_count, user_id)
        )
    else:
        new_user_count = 1
        cursor.execute(
            "INSERT INTO user_clicks (user_id, clicks) VALUES (?, ?)", (user_id, new_user_count)
        )

    db.commit()
    return jsonify({"total_clicks": new_count, "user_clicks": new_user_count})


if __name__ == "__main__":
    init_db()
    app.run(host="0.0.0.0", port=12345)
