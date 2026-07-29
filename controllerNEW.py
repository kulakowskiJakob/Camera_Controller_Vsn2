from camera import Camera

class Controller:

    def __init__(self):

        self.camera = Camera()

    def start(self):

        self.camera.start()

    def stop(self):

        self.camera.stop()

    