from flask import Response

class Streamer:
    def __init__(self, camera):
        self.camera = camera

    def generate(self):
        while True:
            chunk = self.camera.get_h264_chunk()
            if chunk:
                yield chunk

    def response(self):
        return Response(self.generate(), mimetype="video/H264")