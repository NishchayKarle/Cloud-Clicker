import os
import sqlite3

from flask import Flask, Response, g, jsonify, render_template, request
from flask_jwt_extended import (JWTManager, create_access_token,
                                get_jwt_identity, verify_jwt_in_request)
from werkzeug.security import check_password_hash, generate_password_hash

# Initialize the Flask app
app = Flask(__name__)
# For simplicity, I am using a static secret key here.
app.config["JWT_SECRET_KEY"] = "my_secret_key"

# Initialize the JWTManager
jwt = JWTManager(app)

# Path to the SQLite database file
DATABASE = os.path.join(app.root_path, "db", "cloud_clicker.db")


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


# Serve the main page
@app.route("/")
def index():
    return render_template("index.html")


# Serve the clicks page
@app.route("/clicks")
def clicks():
    return render_template("clicks.html")


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

    if user and check_password_hash(user[2], password):
        access_token = create_access_token(identity={"user_id": user[0], "username": username})
        return jsonify(access_token=access_token)
    else:
        return jsonify({"msg": "Bad username or password"}), 401


# API endpoint to get the click count and to increment the click count
@app.route("/api/clicks", methods=["GET", "POST"])
def handle_clicks() -> Response:
    """
    Get the click count or increment the click count.

    GET: Returns the total click count and, if authenticated, the user's click count.
    POST: Increments the total click count and the user's click count (requires authentication).

    Returns:
        JSON: A JSON object with the click counts.
    """
    db = get_db()
    cursor = db.cursor()

    # Get the click count
    if request.method == "GET":
        verify_jwt_in_request(optional=True)

        # Check if auth token is present
        identity = get_jwt_identity()

        # If auth token is present, get the user's click count
        if identity:
            # Get the user ID from the token and fetch the user's click count
            user_id = identity["user_id"]
            cursor.execute("SELECT clicks FROM user_clicks WHERE user_id = ?", (user_id,))
            user_click_data = cursor.fetchone()
            user_clicks = user_click_data[0] if user_click_data else 0

            # Fetch the total click count
            cursor.execute("SELECT count FROM clicks WHERE id = 1")
            click_data = cursor.fetchone()

            return jsonify({"total_clicks": click_data[0], "user_clicks": user_clicks})

        # If auth token is not present, return the total click count
        else:
            # Fetch the total click count
            cursor.execute("SELECT count FROM clicks WHERE id = 1")
            click_data = cursor.fetchone()

            return jsonify({"total_clicks": click_data[0]})

    # Increment the click count
    elif request.method == "POST":
        # make sure auth token is present
        verify_jwt_in_request()

        # Check if auth token is present
        identity = get_jwt_identity()

        # If auth token is not present, return an error
        # The user needs to be authenticated to increment the click count
        if not identity:
            return jsonify({"msg": "Token required"}), 401

        # Get the user ID from the token and increment the click counts
        user_id = identity["user_id"]
        cursor.execute("SELECT count FROM clicks WHERE id = 1")
        click_data = cursor.fetchone()
        new_count = click_data[0] + 1

        # Update the total click count
        cursor.execute("UPDATE clicks SET count = ? WHERE id = 1", (new_count,))

        cursor.execute("SELECT clicks FROM user_clicks WHERE user_id = ?", (user_id,))
        user_click_data = cursor.fetchone()

        # If the user has clicked before, increment the count
        if user_click_data:
            new_user_count = user_click_data[0] + 1
            cursor.execute(
                "UPDATE user_clicks SET clicks = ? WHERE user_id = ?", (new_user_count, user_id)
            )

        # If the user is clicking for the first time, add a new entry
        else:
            new_user_count = 1
            cursor.execute(
                "INSERT INTO user_clicks (user_id, clicks) VALUES (?, ?)", (user_id, new_user_count)
            )

        # Commit the changes to the database
        db.commit()

        return jsonify({"total_clicks": new_count, "user_clicks": new_user_count})


# debug
# list all users
@app.route("/api/users", methods=["GET"])
def get_users() -> Response:
    db = get_db()
    cursor = db.cursor()
    cursor.execute("SELECT * FROM users")
    users = cursor.fetchall()
    return jsonify({"users": users})


if __name__ == "__main__":
    init_db()
    app.run(host="0.0.0.0", port=12345)
