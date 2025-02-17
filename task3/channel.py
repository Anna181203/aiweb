## channel.py - a simple message channel
##

from flask import Flask, request, jsonify
import json
import requests
from datetime import datetime, timedelta


# Class-based application configuration
class ConfigClass(object):
    """ Flask application config """

    # Flask settings
    SECRET_KEY = 'This is an INSECURE secret!! DO NOT use this in production!!'  # change to something random, no matter what


# Create Flask app
app = Flask(__name__)
app.config.from_object(__name__ + '.ConfigClass')  # configuration
app.app_context().push()  # create an app context before initializing db

HUB_URL = 'http://127.0.0.1:5555'
HUB_AUTHKEY = '1234567890'
CHANNEL_AUTHKEY = '0987654321'
CHANNEL_NAME = "Minecraft - Cool Redstone Craftings"
CHANNEL_ENDPOINT = "http://127.0.0.1:5001"  # don't forget to adjust in the bottom of the file
CHANNEL_FILE = 'messages.json'
CHANNEL_TYPE_OF_SERVICE = 'aiweb24:chat'

# Maximum number of messages to store
MAX_MESSAGES = 1

# Maximum message age (e.g., 1 day)
MAX_AGE = timedelta(days=1)


# Function to filter messages by age
def filter_messages_by_age(messages):
    # Get the current time
    current_time = datetime.now()

    # Keep only messages within the MAX_AGE limit
    return [msg for msg in messages if datetime.fromisoformat(msg['timestamp']) > current_time - MAX_AGE]


# Function to read and limit messages
def read_messages():
    global CHANNEL_FILE
    try:
        with open(CHANNEL_FILE, 'r') as f:
            messages = json.load(f)
    except (FileNotFoundError, json.decoder.JSONDecodeError):
        return []

    # Filter messages by age
    messages = filter_messages_by_age(messages)

    # Limit the number of messages to MAX_MESSAGES
    return messages[-MAX_MESSAGES:]


# Function to save messages
def save_messages(messages):
    global CHANNEL_FILE
    # Trim messages to the maximum number
    messages = messages[-MAX_MESSAGES:]

    with open(CHANNEL_FILE, 'w') as f:
        json.dump(messages, f)


@app.cli.command('register')
def register_command():
    global CHANNEL_AUTHKEY, CHANNEL_NAME, CHANNEL_ENDPOINT

    # send a POST request to server /channels
    response = requests.post(HUB_URL + '/channels', headers={'Authorization': 'authkey ' + HUB_AUTHKEY},
                             data=json.dumps({
                                 "name": CHANNEL_NAME,
                                 "endpoint": CHANNEL_ENDPOINT,
                                 "authkey": CHANNEL_AUTHKEY,
                                 "type_of_service": CHANNEL_TYPE_OF_SERVICE,
                             }))

    if response.status_code != 200:
        print("Error creating channel: " + str(response.status_code))
        print(response.text)
        return


def check_authorization(request):
    global CHANNEL_AUTHKEY
    # check if Authorization header is present
    if 'Authorization' not in request.headers:
        return False
    # check if authorization header is valid
    if request.headers['Authorization'] != 'authkey ' + CHANNEL_AUTHKEY:
        return False
    return True


@app.route('/health', methods=['GET'])
def health_check():
    global CHANNEL_NAME
    if not check_authorization(request):
        return "Invalid authorization", 400
    return jsonify({'name': CHANNEL_NAME}), 200


# GET: Return list of messages along with a welcome message
@app.route('/', methods=['GET'])
def home_page():
    if not check_authorization(request):
        return "Invalid authorization", 400

    # Define the welcome message
    welcome_message = {
        "content": "Welcome to the Minecraft - Cool Redstone Craftings channel! 🎮✨\n"
                   "Here, you can share your amazing Redstone creations and discuss with other Minecraft enthusiasts. "
                   "Please be respectful, have fun, and explore all the creative possibilities in Minecraft!",
        "sender": "System",
        "timestamp": datetime.now().isoformat(),  # Current timestamp
        "extra": None
    }

    # Fetch messages and add the welcome message
    messages = read_messages()
    messages.insert(0, welcome_message)  # Add the welcome message at the start of the list

    return jsonify(messages)


# POST: Send a message
@app.route('/', methods=['POST'])
def send_message():
    # Check authorization header
    if not check_authorization(request):
        return "Invalid authorization", 400

    # Check if message is present
    message = request.json
    if not message:
        return "No message", 400
    if 'content' not in message:
        return "No content", 400
    if 'sender' not in message:
        return "No sender", 400
    if 'timestamp' not in message:
        return "No timestamp", 400
    if 'extra' not in message:
        extra = None
    else:
        extra = message['extra']

    # Add message to messages
    messages = read_messages()
    messages.append({
        'content': message['content'],
        'sender': message['sender'],
        'timestamp': message['timestamp'],
        'extra': extra,
    })
    save_messages(messages)
    return "OK", 200


# Start development web server
# run flask --app channel.py register
# to register channel with hub

if __name__ == '__main__':
    app.run(port=5001, debug=True)
