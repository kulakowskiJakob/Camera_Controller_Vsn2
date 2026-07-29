import json
import time
import requests

class Uploader:
    def __init__(self, url):
        self.url = url

    def upload(self, chunk, frame_id):
        metadata = {
            "timestamp": time.time(),
            "frame_id": frame_id
        }

        files = {
            "files": ("frame.h264", chunk, "video/H264")
        }

        data = {
            "metadata": json.dumps(metadata)
        }

        requests.post(self.url, files=files, data=data)