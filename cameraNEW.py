from picamera2 import Picamera2
from picamera2.encoders import H264Encoder
from picamera2.outputs import CircularOutput

class Camera:
    def __init__(self, width=1280, height=720, bitrate=2000000):
        self.width = width
        self.height = height
        self.bitrate = bitrate

        self.camera = Picamera2()
        config = self.camera.create_video_configuration(
            main={"size": (width, height)}
        )
        self.camera.configure(config)

        # H.264 hardware encoder
        self.encoder = H264Encoder(bitrate=self.bitrate)

        # Circular output allows continuous streaming
        self.output = CircularOutput(buffersize=4)

        self.frame_id = 0

        # Start recording immediately
        self.camera.start_recording(self.encoder, self.output)

    def get_h264_chunk(self):
        # Read encoded H.264 data
        data = self.output.read()
        self.frame_id += 1
        return data

    def stop(self):
        self.camera.stop_recording()
        self.camera.close()
        