from picamera2 import Picamera2
from picamera2.encoders import H264Encoder
import subprocess
import threading
import io

class Camera:
    def __init__(self, width=1280, height=720, bitrate=2000000):
        self.width = width
        self.height = height
        self.bitrate = bitrate

        self.buffer = io.BytesIO()
        self.lock = threading.Lock()

        self.picam2 = Picamera2()
        config = self.picam2.create_video_configuration(
            main={"size": (width, height)}
        )
        self.picam2.configure(config)

        self.encoder = H264Encoder(bitrate=self.bitrate)

        # Start FFmpeg that converts raw H.264 → fragmented MP4
        self.ffmpeg = subprocess.Popen([
            "ffmpeg",
            "-i", "pipe:0",          # input comes from stdin
            "-c:v", "copy",          # do not re-encode (keeps hardware acceleration)
            "-f", "mp4",
            "-movflags", "frag_keyframe+empty_moov+default_base",
            "pipe:1"                 # output fMP4 to stdout
        ], stdin=subprocess.PIPE, stdout=subprocess.PIPE)

        # Start Picamera2 recording, writing H.264 to ffmpeg stdin
        self.picam2.start_recording(self.encoder, self.ffmpeg.stdin)

        # Thread to read from ffmpeg stdout into buffer
        threading.Thread(target=self._reader_thread, daemon=True).start()

    def _reader_thread(self):
        while True:
            data = self.ffmpeg.stdout.read(4096)
            if not data:
                break
            with self.lock:
                self.buffer.write(data)

    def get_fragment(self):
        with self.lock:
            data = self.buffer.getvalue()
            self.buffer.seek(0)
            self.buffer.truncate(0)
        return data

    def stop(self):
        self.picam2.stop_recording()
        self.ffmpeg.stdin.close()
        self.ffmpeg.terminate()
        self.ffmpeg.wait()
