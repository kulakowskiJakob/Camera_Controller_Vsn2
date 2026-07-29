from picamera2 import Picamera2
from picamera2.encoders import H264Encoder
from pipe_output import MP4BoxFragmenter

class Camera:
    def __init__(self):
        self.picam2 = Picamera2()
        config = self.picam2.create_video_configuration()
        self.picam2.configure(config)

        self.output = MP4BoxFragmenter()
        self.encoder = H264Encoder(bitrate=2000000)

        self.picam2.start_recording(self.encoder, self.output)

    def get_fragment(self):
        return self.output.get_fragment()

    def stop(self):
        self.picam2.stop_recording()
        self.output.close()
