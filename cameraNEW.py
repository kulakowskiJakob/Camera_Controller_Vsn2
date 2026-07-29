from picamera2 import Picamera2
from picamera2.encoders import H264Encoder
from picamera2.outputs import FfmpegOutput

class Camera:

    def __init__(self):

        self.camera = Picamera2()
        config = self.camera.create_video_configuration(
            main={
                "size": (1280,720),
                "format": "RGB888"
            }
        )

        self.camera.configure(config)
        self.encoder = H264Encoder(
            bitrate=8000000
        )

    def start(self):

        self.camera.start_recording(
            self.encoder,
            FfmpegOutput(
                "hls/index.m3u8"
            )
        )

    def stop(self):

        self.camera.stop_recording()
        