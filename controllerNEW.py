import threading
import time

class Controller:
    def __init__(self, camera, uploader):
        self.camera = camera
        self.uploader = uploader
        self.running = False
        self.thread = None

    def start(self):
        if self.running:
            return
        self.running = True
        self.thread = threading.Thread(target=self.run)
        self.thread.start()

    def stop(self):
        self.running = False

    def run(self):
        while self.running:
            chunk = self.camera.get_h264_chunk()
            if chunk:
                self.uploader.upload(chunk, self.camera.frame_id)
            time.sleep(0.01)