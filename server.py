from flask import Flask
from subprocess import Popen
from threading import Thread

app = Flask(__name__)

@app.route('/')
def index():
    # Return the HTML page
    with open('index.html', 'r') as f:
        return f.read()

@app.route('/start_motion_detection')
def start_motion_detection():
    # Execute the Python program in a separate thread
    t = Thread(target=start_motion_detection_thread)
    t.start()
    return 'Motion detection started.'

def start_motion_detection_thread():
    # Execute the Python program
    Popen(['python', 'motion_detection.py'])

if __name__ == '__main__':
    app.run(host='localhost', port=8000)
