from flask import Flask, render_template, redirect, url_for, request, session
import os
import cgi
import datetime
import time
import json

app = Flask(__name__)

# SETTINGS
app.config['DEBUG'] = True
app.config['PUSHER_CHAT_APP_ID'] = '207136'
app.config['PUSHER_CHAT_APP_KEY'] = 'aa578c9a158782bff5f5'
app.config['PUSHER_CHAT_APP_SECRET'] = '54c667c6a791f308640b'
app.config['SECRET_KEY'] = "\x81\xa8\xcb\x8fl\x15\x16\xbfJ\xc3\xeb\x90\xfe\x82e\xdaS\x07\x95N\xa7\xb4\x95"

import pusher

pusher_client = pusher.Pusher(
  app_id=app.config['PUSHER_CHAT_APP_ID'],
  key=app.config['PUSHER_CHAT_APP_KEY'],
  secret=app.config['PUSHER_CHAT_APP_SECRET'],
  ssl=True
)

@app.route("/")
def index():
    return render_template('index.html')

@app.route("/setname/", methods=["POST"])
def set_name():
    session['name'] = request.form['name']
    
    return "Successful"

@app.route("/pusher/auth/", methods=["POST"])
def pusher_authentication():
    auth = pusher_client.authenticate(
        channel = request.form['channel_name'],
        socket_id = request.form['socket_id'],
        custom_data = {
            'user_id': session['name'],
        }
    )
    
    return json.dumps(auth)

@app.route("/messages/", methods=["POST"])
def new_message():
    name = request.form['name']
    text = cgi.escape(request.form['text'])
    channel = request.form['channel']
    
    now = datetime.datetime.now()
    timestamp = time.mktime(now.timetuple()) * 1000
    pusher_client.trigger("presence-" + channel, 'new_message', {
        'text': text,
        'name': name,
        'time': timestamp
    })
    
    return "Successful"
    
    
if __name__ == "__main__":
    # Have to set host and port since using Cloud9; don't need if running locally or on a server
    host = os.getenv('IP','0.0.0.0')
    port = int(os.getenv('PORT', 5000))
    app.run(host=host, port=port)
    