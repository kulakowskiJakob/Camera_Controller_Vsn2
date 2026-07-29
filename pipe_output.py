from picamera2.outputs import Output
import subprocess
import threading
import io

class FFmpegFragmenter(Output):
    def __init__(self):
        super().__init__()
        self.buffer = io.BytesIO()
        self.lock = threading.Lock()

        self.ffmpeg = subprocess.Popen([
            "ffmpeg",
            "-i", "pipe:0",
            "-c:v", "copy",
            "-f", "mp4",
            "-movflags", "frag_keyframe+empty_moov+default_base",
            "pipe:1"
        ], stdin=subprocess.PIPE, stdout=subprocess.PIPE)

        assert self.ffmpeg.stdin is not None
        assert self.ffmpeg.stdout is not None

        threading.Thread(target=self._reader, daemon=True).start()

    def _reader(self):
        while True:
            data = self.ffmpeg.stdout.read(4096)
            if not data:
                break
            with self.lock:
                self.buffer.write(data)

    def outputframe(self, frame, *args, **kwargs):
        # Picamera2 may pass 6 args; we ignore them.
        try:
            self.ffmpeg.stdin.write(frame)
        except BrokenPipeError:
            pass

    def get_fragment(self):
        with self.lock:
            data = self.buffer.getvalue()
            self.buffer.seek(0)
            self.buffer.truncate(0)
        return data

    def close(self):
        try:
            self.ffmpeg.stdin.close()
        except:
            pass
        self.ffmpeg.terminate()
