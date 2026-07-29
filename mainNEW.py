from flask import Flask
from controller import Controller
from streamer import Streamer

app = Flask(__name__)
controller = Controller()
controller.start()
Streamer(app)

@app.route("/")
def index():

    return open("templates/index.html").read()

app.run(
    host="0.0.0.0",
    port=5000
)