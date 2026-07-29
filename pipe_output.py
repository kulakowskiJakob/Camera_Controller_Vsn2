from picamera2.outputs import Output
import subprocess
import threading
import io

class MP4BoxFragmenter(Output):
    def __init__(self):
        super().__init__()

        self.buffer = io.BytesIO()
        self.lock = threading.Lock()

        # Real-time MP4 fragmenter using GPAC / MP4Box
        self.mp4box = subprocess.Popen([
            "MP4Box",
            "-add", "pipe:1:fmt=h264",
            "-new", "-",              # produce fMP4 to stdout
            "-frag", "1000"           # 1ms fragment interval (fast)
        ], stdin=subprocess.PIPE, stdout=subprocess.PIPE)

        assert self.mp4box.stdin is not None
        assert self.mp4box.stdout is not None

        threading.Thread(target=self._reader_thread, daemon=True).start()

    def _reader_thread(self):
        while True:
            data = self.mp4box.stdout.read(4096)
            if not data:
                break

            with self.lock:
                self.buffer.write(data)

    def outputframe(self, frame, *args, **kwargs):
        try:
            self.mp4box.stdin.write(frame)
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
            self.mp4box.stdin.close()
        except:
            pass
        self.mp4box.terminate()
