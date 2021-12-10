import os
import threading

import flask

HOST = "0.0.0.0"
d_path = os.path.abspath(os.path.dirname(__file__))
html_folder_path = os.path.join(d_path, "template")
static_folder_path = os.path.join(d_path, "static")

app = flask.Flask(__name__)

"""-------------------UTILS-------------------"""


def run_flask_app():
    """
    Creates Flask server.
    :return:
    """
    print("- Start Server")
    app.run(host=HOST, port=5000, threaded=True)


"""-------------------ROUTES-------------------"""


@app.route("/", methods=["GET"])
def get_index():
    return flask.render_template("index.html")


@app.route("/version", methods=["GET"])
def get_version():
    return flask.render_template("version.html")


@app.route("/script_status", methods=["POST"])
def post_scipt_status():
    return flask.render_template("index.html")


@app.route("/end")
def end():
    return flask.render_template("index.html")


"""-------------------END ROUTES-------------------"""


if __name__ == "__main__":
    threading.Thread(target=run_flask_app).start()
    # webbrowser.open('http://127.0.0.1:5000/')
