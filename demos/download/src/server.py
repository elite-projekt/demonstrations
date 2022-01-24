import os
import threading
import requests

import flask
from flask import send_from_directory

HOST = "0.0.0.0"  # nosec No Issue in a docker Container
d_path = os.path.abspath(os.path.dirname(__file__))
static_folder_path = os.path.join(d_path, "static")

app = flask.Flask(__name__, static_url_path='/static')

"""-------------------UTILS-------------------"""


def run_flask_app():
    """
    Creates Flask server.
    :return:
    """
    print("- Start Server")
    app.run(host=HOST, port=5001, threaded=True)


"""-------------------ROUTES-------------------"""


@app.route("/", methods=["GET"])
def get_index():
    return send_from_directory("static", "template.html")


@app.route("/<path:path>", methods=["GET"])
def static_dir(path):
    return send_from_directory("static", path)


@app.route("/version", methods=["GET"])
def get_version():
    return send_from_directory("static", "version.html")


@app.route("/unsecure", methods=["POST"])
def post_scipt_status():
    r = requests.post(
        'http://host.docker.internal:5000/' +
        'orchestration/download/create_fake_malware'
    )
    return "native app response: HTTP " + str(r.status_code)


@app.route("/end")
def end():
    return send_from_directory("static", "template.html")


"""-------------------END ROUTES-------------------"""


if __name__ == "__main__":
    threading.Thread(target=run_flask_app).start()
    # webbrowser.open('http://127.0.0.1:5001/')
