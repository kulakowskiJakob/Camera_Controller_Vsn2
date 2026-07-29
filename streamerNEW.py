from flask import send_from_directory

class Streamer:

    def __init__(self, app):

        self.app = app

        @app.route("/hls/<path:filename>")
        def hls(filename):

            return send_from_directory(
                "hls",
                filename
            )
        