from flask import Flask, render_template, request
from chatterbot import ChatBot
from chatterbot.trainers import ListTrainer
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
   # database_uri=f'mysql+mysqlconnector://{MYSQL_USER}:{MYSQL_PASSWORD}@{MYSQL_HOST}/{MYSQL_DB}'
    database_uri='sqlite:///database.sqlite3'
)

# Create a new trainer
trainer = ListTrainer(bot)

# Read data from the file and train the bot
with open('data.txt', 'r') as file:
    conversations = file.readlines()

for conversation in conversations:
    pair = conversation.strip().split('\t')
    trainer.train(pair)

# Additional training with custom conversations
# trainer.train([
#     "Hi",
#     "Welcome, friend 🤗 my name is shivam I am here to assist you",
#     "i'm pretty good. thanks for asking"
# ])

@app.route("/")
def home():
    return render_template("index.html")

@app.route("/get_response", methods=["POST"])
def get_response():
    user_message = request.form.get("message")
    response = bot.get_response(user_message)
    return str(response)

if __name__ == "__main__":
    app.run(debug=True ,host='0.0.0.0')
