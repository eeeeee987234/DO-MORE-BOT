from flask import Flask
from threading import Thread
import os

app = Flask(__name__)

@app.route('/')
def home():
    return "DoEA Console is running!"

@app.route('/health')
def health():
    return "OK"

@app.route('/ping')
def ping():
    return "pong"

def run():
    print("Starting Flask on port 8000...")
    app.run(host='0.0.0.0', port=8000, debug=False)

def keep_alive():
    t = Thread(target=run)
    t.daemon = True
    t.start()
    print("Flask thread started")
