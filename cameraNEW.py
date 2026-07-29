from picamera2 import Picamera2
from picamera2.encoders import H264Encoder
from picamera2.outputs import FileOutput
import io

class Camera:
    def __init__(self, width=1280, height=720, bitrate=2000000):
        self.width = width
        self.height = height

        self.picam2 = Picamera2()
        config = self.picam2.create_video_configuration(
            main={"size": (width, height)}
        )
        self.picam2.configure(config)

        # Use H.264 hardware encoder
        self.encoder = H264Encoder(bitrate=bitrate)

        # Use BytesIO as an in-memory output buffer
        self.buffer = io.BytesIO()
        self.output = FileOutput(self.buffer)

        self.frame_id = 0

        self.picam2.start_recording(self.encoder, self.output)

    def get_h264_chunk(self):
        # Get current buffer contents
        data = self.buffer.getvalue()

        # Clear buffer so only new data appears next call
        self.buffer.seek(0)
        self.buffer.truncate(0)

        if data:
            self.frame_id += 1
            return data

        return None

    def stop(self):
        self.picam2.stop_recording()
        self.picam2.close()
