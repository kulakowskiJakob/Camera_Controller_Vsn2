from flask import Flask, jsonify

from camera import Camera
from streamer import Streamer
from uploader import Uploader
from controller import Controller

app = Flask(__name__)

camera = Camera() 
streamer = Streamer(camera)
uploader = Uploader(
    "http:/localhost:8000/frame"
)
controller = Controller(
    camera,
    uploader
)
@app.route("/start")
def start():

    controller.start()
    return jsonify({
        "status": True
    })
@app.route("/stop")
def stop():

    controller.stop()
    return jsonify({
        "status": False
    })
@app.route("/video")
def video():
    
    return streamer.response()

if __name__ == "__main__":

    app.run(
        host="0.0.0.0",
        port=5000,
        threaded=True
    )