import flask

native = flask.Blueprint("native", __name__, url_prefix="/native/")


@native.route("/native/getdemos", methods=["GET"])
def getDemos():
    data = flask.json.load(open("native/nativeapp/demos.json",
                                encoding="utf-8"))
    return flask.jsonify(data)
