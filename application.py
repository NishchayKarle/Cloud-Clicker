import logging
import os
import sqlite3
from logging.handlers import RotatingFileHandler

from flask import Flask, Response, g, jsonify, render_template, request
from flask_jwt_extended import (JWTManager, create_access_token,
                                get_jwt_identity, verify_jwt_in_request)
from werkzeug.security import check_password_hash, generate_password_hash

# Initialize the Flask app
app = Flask(__name__, static_folder="static", template_folder="templates")
# For simplicity, I am using a static secret key here.
app.config["JWT_SECRET_KEY"] = "my_secret_key"

# Initialize the JWTManager
jwt = JWTManager(app)

# Path to the SQLite database file
DATABASE = os.path.join(app.root_path, "db", "cloud_clicker.db")

# Set up logging
if not os.path.exists("logs"):
    os.makedirs("logs")

file_handler = RotatingFileHandler(
    os.path.join(app.root_path, "logs", "app.log"),
    maxBytes=10240,
    backupCount=10,
)
file_handler.setFormatter(
    logging.Formatter(
        "%(asctime)s %(levelname)s: %(message)s [in %(pathname)s:%(lineno)d]"
    )
)
file_handler.setLevel(logging.INFO)
app.logger.addHandler(file_handler)
app.logger.setLevel(logging.INFO)
app.logger.info("Cloud Clicker Application Startup")


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


# @app.before_request
# def log_request_info():
#     """Log the request information before processing a request."""
#     app.logger.info("Headers: %s", request.headers)
#     app.logger.info("Body: %s", request.get_data())


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
        JSON: A JSON object with a message indicating
                the success or failure of the registration.
    """
    # Get the username and password from the request
    data = request.get_json()
    username = data.get("username")
    password = data.get("password")
    # Generate a hash for the password
    hashed_password = generate_password_hash(password)

    db = get_db()
    cursor = db.cursor()
    try:
        # Insert the user details into the database
        cursor.execute(
            "INSERT INTO users (username, password) VALUES (?, ?)",
            (
                username,
                hashed_password,
            ),
        )

        # Initialze click count for the new user
        user_id = cursor.lastrowid
        # Insert initial click count for the new user
        cursor.execute(
            "INSERT INTO user_clicks (user_id, clicks) VALUES (?, ?)",
            (
                user_id,
                0,
            ),
        )

        db.commit()
        app.logger.info(f"User {username} registered successfully.")

    except sqlite3.IntegrityError:
        app.logger.error(f"Username {username} already exists.")
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
    # Get the username and password from the request
    data = request.get_json()
    username = data.get("username")
    password = data.get("password")

    db = get_db()
    cursor = db.cursor()
    cursor.execute(
        "SELECT * FROM users WHERE username = ?", (username,)
    )  # Check if the username exists
    user = cursor.fetchone()

    # If the user exists and the password is correct, generate an access token
    if user and check_password_hash(user[2], password):
        access_token = create_access_token(
            identity={
                "user_id": user[0],
                "username": username,
            }
        )
        app.logger.info(f"User {username} logged in successfully.")
        return jsonify(access_token=access_token)

    else:
        app.logger.warning(f"Failed login attempt for username {username}.")
        return jsonify({"msg": "Bad username or password"}), 401


# API endpoint to get the click count and to increment the click count
@app.route("/api/clicks", methods=["GET", "POST"])
def handle_clicks() -> Response:
    """
    Get the click count or increment the click count.

    GET: Returns the total click count and,
        if authenticated, the user's click count.
    POST: Increments the total click count and,
        the user's click count (requires authentication).

    Returns:
        JSON: A JSON object with the click counts.
    """
    db = get_db()
    cursor = db.cursor()

    # Get the click count
    if request.method == "GET":
        verify_jwt_in_request(optional=True)

        # Fetch the total click count
        cursor.execute("SELECT count FROM clicks WHERE id = 1")
        click_data = cursor.fetchone()
        total_clicks = click_data[0] if click_data else 0

        # Check if auth token is present
        identity = get_jwt_identity()

        # If auth token is present, get the user's click count
        if identity:
            # Get the user ID from the token and fetch the user's click count
            user_id = identity["user_id"]
            cursor.execute(
                "SELECT clicks FROM user_clicks WHERE user_id = ?",
                (user_id,),
            )
            user_click_data = cursor.fetchone()
            user_clicks = user_click_data[0] if user_click_data else 0

            return jsonify(
                {"total_clicks": total_clicks, "user_clicks": user_clicks}
            )

        # If auth token is not present, return the total click count
        else:
            return jsonify({"total_clicks": total_clicks})

    # Increment the click count
    elif request.method == "POST":
        # make sure auth token is present
        verify_jwt_in_request()

        # Check if auth token is present
        identity = get_jwt_identity()

        # If auth token is not present, return an error
        # The user needs to be authenticated to increment the click count
        if not identity:
            app.logger.warning("Unauthorized try to increment click counts.")
            return jsonify({"msg": "Token required"}), 401

        # Get the user ID from the token and increment the click counts
        user_id = identity["user_id"]
        cursor.execute("SELECT count FROM clicks WHERE id = 1")
        click_data = cursor.fetchone()
        new_count = click_data[0] + 1

        # Update the total click count
        cursor.execute(
            "UPDATE clicks SET count = ? WHERE id = 1",
            (new_count,),
        )

        cursor.execute(
            "SELECT clicks FROM user_clicks WHERE user_id = ?",
            (user_id,),
        )

        # Increment the user's click count
        # New users will have a click count of 0 initialized at registration
        user_click_data = cursor.fetchone()
        new_user_count = user_click_data[0] + 1
        cursor.execute(
            "UPDATE user_clicks SET clicks = ? WHERE user_id = ?",
            (
                new_user_count,
                user_id,
            ),
        )

        # Commit the changes to the database
        db.commit()
        app.logger.info(
            f'User {identity["username"]} incremented click counts.'
        )
        return jsonify(
            {
                "total_clicks": new_count,
                "user_clicks": new_user_count,
            }
        )


def main():
    try:
        init_db()

    except sqlite3.OperationalError:
        app.logger.error("Database connection failed. Exiting...")
        exit(1)

    except Exception as e:
        app.logger.error(f"An error occurred: {e}")
        exit(1)


main()
