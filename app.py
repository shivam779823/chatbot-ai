from flask import Flask, request, jsonify
from chatterbot import ChatBot
from chatterbot.trainers import ChatterBotCorpusTrainer
import os 

app = Flask(__name__)

MYSQL_HOST = os.environ.get("MYSQL_HOST", "ubuntu")
MYSQL_USER = os.environ.get("MYSQL_USER", "test")
MYSQL_PASSWORD = os.environ.get("MYSQL_PASSWORD", "12345678")
MYSQL_DB = os.environ.get("MYSQL_DB", "pharmaco")

# Create a new ChatBot instance
bot = ChatBot(
    'pharmaco',
    storage_adapter='chatterbot.storage.SQLStorageAdapter',
    #database_uri=f'mysql+mysqlconnector://{MYSQL_USER}:{MYSQL_PASSWORD}@{MYSQL_HOST}/{MYSQL_DB}'
    database_uri='sqlite:///database.sqlite3'
)

# Create a new trainer for the chatbot
trainer = ChatterBotCorpusTrainer(bot)

trainer.train("./custom.yaml")
# Train based on english greetings corpus
trainer.train("chatterbot.corpus.english.greetings")

@app.route("/")
def home():
    return "Chatbot API is running."

@app.route("/api/get_response", methods=["POST"])
def get_response():
    default = "Hi How can I help you Today"
    user_message = request.json.get("message")
    if not user_message:
        return jsonify(response=default)
    print(f"Received message: {user_message}")  # Log received message
    response = bot.get_response(user_message)
    print(f"Bot response: {response}")  # Log bot response
    return jsonify(response=str(response))

if __name__ == "__main__":
    app.run(debug=True, host='0.0.0.0', port=5001)



























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
