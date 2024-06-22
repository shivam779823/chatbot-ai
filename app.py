from flask import Flask, request, jsonify
from chatterbot import ChatBot
from chatterbot.trainers import ChatterBotCorpusTrainer, ListTrainer
import mysql.connector
import yaml
import os

app = Flask(__name__)

# MySQL database configuration from environment variables
MYSQL_HOST = os.environ.get("MYSQL_HOST", "localhost")
MYSQL_USER = os.environ.get("MYSQL_USER", "test")
MYSQL_PASSWORD = os.environ.get("MYSQL_PASSWORD", "12345678")
MYSQL_DB = os.environ.get("MYSQL_DB", "pharmaco")

def get_db_connection():
    """Create and return a new MySQL database connection."""
    return mysql.connector.connect(
        host=MYSQL_HOST,
        user=MYSQL_USER,
        password=MYSQL_PASSWORD,
        database=MYSQL_DB
    )

# Create a new ChatBot instance
bot = ChatBot(
    'pharmaco',
    storage_adapter='chatterbot.storage.SQLStorageAdapter',
    database_uri=f'mysql+mysqlconnector://{MYSQL_USER}:{MYSQL_PASSWORD}@{MYSQL_HOST}/{MYSQL_DB}'
)

# Train the chatbot with a basic corpus and custom data
trainer = ChatterBotCorpusTrainer(bot)
trainer.train("chatterbot.corpus.english.greetings")

# Function to load and train custom data from a YAML file
def train_custom_data(file_path):
    with open(file_path, 'r') as stream:
        try:
            custom_data = yaml.safe_load(stream)
            conversations = custom_data.get('conversations', [])
            trainer = ListTrainer(bot)
            for conversation in conversations:
                trainer.train(conversation)
        except yaml.YAMLError as exc:
            print(f"Error reading YAML file: {exc}")

# Train with custom data
train_custom_data("./custom.yaml")

@app.route("/")
def home():
    return "Chatbot API is running."

@app.route("/api/get_response", methods=["POST"])
def get_response():
    default = "Hi, How can I help you today?"
    user_message = request.json.get("message")
    if not user_message:
        return jsonify(response=default)
    
    # Establish a new database connection
    db_connection = get_db_connection()
    cursor = db_connection.cursor(dictionary=True)

    try:
        # Example of querying data from MySQL database
        query = "SELECT name, price, mrp, quantity, expiry FROM medicines WHERE name LIKE %s"
        cursor.execute(query, (f'%{user_message}%',))
        result = cursor.fetchone()

        if result:
            response = f"Here are the details for {result['name']}: Price - {result['price']}, MRP - {result['mrp']}, Quantity - {result['quantity']}, Expiry - {result['expiry'].strftime('%Y-%m-%d')}"
        else:
            response = str(bot.get_response(user_message))
    except Exception as e:
        response = f"An error occurred: {str(e)}"
    finally:
        # Close the cursor and the database connection
        cursor.close()
        db_connection.close()

    return jsonify(response=response)

if __name__ == "__main__":
    app.run(debug=True, host='0.0.0.0', port=int(os.environ.get('PORT', 8081)))





# from flask import Flask, request, jsonify
# from chatterbot import ChatBot
# from chatterbot.trainers import ChatterBotCorpusTrainer
# import requests
# import os 

# app = Flask(__name__)

# MYSQL_HOST = os.environ.get("MYSQL_HOST", "ubuntu")
# MYSQL_USER = os.environ.get("MYSQL_USER", "test")
# MYSQL_PASSWORD = os.environ.get("MYSQL_PASSWORD", "12345678")
# MYSQL_DB = os.environ.get("MYSQL_DB", "pharmaco")

# # Create a new ChatBot instance
# bot = ChatBot(
#     'pharmaco',
#     storage_adapter='chatterbot.storage.SQLStorageAdapter',
#     database_uri=f'mysql+mysqlconnector://{MYSQL_USER}:{MYSQL_PASSWORD}@{MYSQL_HOST}/{MYSQL_DB}'
#     #database_uri='sqlite:///database.sqlite3'
# )

# # Train the chatbot with a basic corpus
# trainer = ChatterBotCorpusTrainer(bot)
# trainer.train("chatterbot.corpus.english.greetings")
# trainer.train("./custom.yaml")


# @app.route("/")
# def home():
#     return "Chatbot API is running."

# @app.route("/api/get_response", methods=["POST"])
# def get_response():
#     default = "Hi How can I help you Today"
#     user_message = request.json.get("message")
#     if not user_message:
#         return jsonify(response=default)
#     response = bot.get_response(user_message)
#     return jsonify(response=str(response))

# @app.route("/ask_bot", methods=["POST"])
# def ask_bot():
#     try:
#         user_message = request.form.get("message")
#         if not user_message:
#             return "Error: No message provided", 400

#         headers = {'Content-Type': 'application/json'}
#         response = requests.post("http://pharmaco-chatbot-service:81/api/get_response", json={"message": user_message}, headers=headers, timeout=5)
#         response_json = response.json()
#         return response_json.get("response", "Error: No response from bot")
#     except requests.exceptions.RequestException as e:
#         return f"Error communicating with chatbot: {str(e)}", 500

# if __name__ == "__main__":
#     app.run(debug=True, host='0.0.0.0', port=int(os.environ.get('PORT', 8081)))
















# from flask import Flask, request, jsonify
# from chatterbot import ChatBot
# from chatterbot.trainers import ChatterBotCorpusTrainer
# import os 

# app = Flask(__name__)

# MYSQL_HOST = os.environ.get("MYSQL_HOST", "ubuntu")
# MYSQL_USER = os.environ.get("MYSQL_USER", "test")
# MYSQL_PASSWORD = os.environ.get("MYSQL_PASSWORD", "12345678")
# MYSQL_DB = os.environ.get("MYSQL_DB", "pharmaco")

# # Create a new ChatBot instance
# bot = ChatBot(
#     'pharmaco',
#     storage_adapter='chatterbot.storage.SQLStorageAdapter',
#     #database_uri=f'mysql+mysqlconnector://{MYSQL_USER}:{MYSQL_PASSWORD}@{MYSQL_HOST}/{MYSQL_DB}'
#     database_uri='sqlite:///database.sqlite3'
# )

# # Create a new trainer for the chatbot
# trainer = ChatterBotCorpusTrainer(bot)

# trainer.train("./custom.yaml")
# # Train based on english greetings corpus
# trainer.train("chatterbot.corpus.english.greetings")

# @app.route("/")
# def home():
#     return "Chatbot API is running."

# @app.route("/api/get_response", methods=["POST"])
# def get_response():
#     default = "Hi How can I help you Today"
#     user_message = request.json.get("message")
#     if not user_message:
#         return jsonify(response=default)
#     print(f"Received message: {user_message}")  # Log received message
#     response = bot.get_response(user_message)
#     print(f"Bot response: {response}")  # Log bot response
#     return jsonify(response=str(response))

# if __name__ == "__main__":
#     app.run(debug=True, host='0.0.0.0')



























# from flask import Flask, render_template, request
# from chatterbot import ChatBot
# from chatterbot.trainers import ChatterBotCorpusTrainer
# from collections.abc import Hashable

# import os 

# app = Flask(__name__)

# MYSQL_HOST = os.environ.get("MYSQL_HOST", "ubuntu")
# MYSQL_USER = os.environ.get("MYSQL_USER", "test")
# MYSQL_PASSWORD = os.environ.get("MYSQL_PASSWORD", "12345678")
# MYSQL_DB = os.environ.get("MYSQL_DB", "pharmaco")

# # Create a new ChatBot instance
# bot = ChatBot(
#     'pharmaco',
#     storage_adapter='chatterbot.storage.SQLStorageAdapter',
#     #database_uri=f'mysql+mysqlconnector://{MYSQL_USER}:{MYSQL_PASSWORD}@{MYSQL_HOST}/{MYSQL_DB}'
#     database_uri='sqlite:///database.sqlite3'
# )

# # Create a new trainer for the chatbot
# trainer = ChatterBotCorpusTrainer(bot)

# trainer.train("./custom.yaml")
# # Train based on english greetings corpus
# trainer.train("chatterbot.corpus.english.greetings")



# @app.route("/")
# def home():
#     return render_template("index.html")


# @app.route("/get_response", methods=["POST"])
# def get_response():
#     default = "Hi How can I help you Today"
#     user_message = request.form.get("message")
#     if not user_message:
#         return default
#     print(f"Received message: {user_message}")  # Log received message
#     response = bot.get_response(user_message)
#     print(f"Bot response: {response}")  # Log bot response
#     return str(response)

# if __name__ == "__main__":
#     app.run(debug=True ,host='0.0.0.0')
