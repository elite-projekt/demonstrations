import flask

native = flask.Blueprint("native", __name__, url_prefix="/native/")


@native.route("/getdemos", methods=["GET"])
def getDemos():
    data = flask.json.load(open("demos/demos.json",
                                encoding="utf-8"))
    return flask.jsonify(data)
