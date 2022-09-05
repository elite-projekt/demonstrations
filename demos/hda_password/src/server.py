import threading

import flask
import pathlib
import pyotp
import qrcode

HOST = "0.0.0.0"  # nosec No Issue in a Docker Container
LANGUAGE = "de"
random_id = pyotp.random_hex()
# d_path = os.path.abspath(os.path.dirname(__file__))
# html_folder_path = os.path.join(d_path, "template")
# static_folder_path = os.path.join(d_path, "static")
d_path = pathlib.Path(__file__).parent.absolute()
html_folder_path = pathlib.Path(d_path) / "template"
static_folder_path = pathlib.Path(d_path) / "static"


app = flask.Flask(__name__)
users = {}

"""-------------------UTILS-------------------"""


class User:
    def __init__(self, username, password, otp):
        self.username = username
        self.password = password
        self.otp = otp


def validate_otp(otp, temp_code):
    totp = pyotp.TOTP(otp)
    print(totp.now())
    if totp.now() == temp_code:
        return True
    return False


def create_user(name, pwd, mode):
    user = User(name, pwd, pyotp.random_base32())
    users[mode] = user
    print(
        "New User: "
        + user.username
        + ", PW: "
        + user.password
        + ", Mode: "
        + mode
        + ", OTP_SEED: "
        + user.otp
    )
    return user


def run_flask_app():
    """
    Creates Flask server 2.
    :return:
    """
    print("- Start Server 2")
    app.config.from_pyfile("config.py", silent=True)
    app.run(host=HOST, port="5001", threaded=True)


def create_qr(user_name, otp):
    url = pyotp.totp.TOTP(otp).provisioning_uri(
        name=user_name, issuer_name="Nimbus 2FA Service"
    )
    qr = qrcode.QRCode(
        version=1,
        error_correction=qrcode.constants.ERROR_CORRECT_L,
        box_size=10,
        border=4,
    )
    qr.add_data(url)
    qr.make(fit=True)
    img = qr.make_image(fill_color="black", back_color="white")
    return img


"""-------------------BEGINN SAFE MODE-------------------"""


@app.route("/favicon.ico")
def get_favicon():
    file_path = pathlib.Path(static_folder_path) / "favicon.ico"
    return flask.send_file(file_path)


@app.route("/")
@app.route("/story_intro")
def story_intro_sm():
    if LANGUAGE == "de":
        return flask.render_template("secure/sm1_geschichten_intro.html")
    else:
        return flask.render_template("secure/sm1_story_intro.html")


@app.route("/register_account_services", methods=["POST", "GET"])
def registration_kontodienste_sm():
    if flask.request.method == "POST":
        user_name = flask.request.form["name"]
        user_password = flask.request.form["password"]
        resp = flask.make_response(flask.redirect(
            "/init_2fa_account_services"))
        user = create_user(user_name, user_password, "sm_kd")
        qr_code = create_qr(user_name, user.otp)
        if LANGUAGE == "de":
            qr_code.save(pathlib.Path(static_folder_path) / "qrcode3.jpg")
        else:
            qr_code.save(pathlib.Path(static_folder_path) / "qrcode1.jpg")
        return resp
    else:
        if LANGUAGE == "de":
            return flask.render_template(
                "secure/sm2_registrierung_kontodienste.html")
        else:
            return flask.render_template(
                "secure/sm2_registration_kontodienste.html")


@app.route("/story_2fa")
def story_2fa_sm():
    if LANGUAGE == "de":
        return flask.render_template(
            "secure/sm3_geschichte_2fa.html",
            flash="Erfolgreiche Registrierung!")

    else:
        return flask.render_template(
            "secure/sm3_story_2fa.html",
            flash="Registration succesfull!")


@app.route("/init_2fa_account_services", methods=["POST", "GET"])
def initial_2fa_kontodienste_sm():
    if flask.request.method == "POST":
        validation = flask.request.form["validation"]
        if validate_otp(users.get("sm_kd").otp, validation):
            resp = flask.make_response(
                flask.redirect("story_login"))
            print("Succesfull validate qr")
            return resp
        else:
            print("wrong validation")
            if LANGUAGE == "de":
                return flask.render_template(
                    "secure/sm4_anfaenglich_2fa_kontodienste.html",
                    flash="validation failed!",
                    classes="fade show display",
                )
            else:
                return flask.render_template(
                    "secure/sm4_initial_2fa_kontodienste.html",
                    flash="validation failed!",
                    classes="fade show display",
                )
    else:
        if LANGUAGE == "de":
            return flask.render_template(
                "secure/sm4_anfaenglich_2fa_kontodienste.html")
        else:
            return flask.render_template(
                "secure/sm4_initial_2fa_kontodienste.html")


@app.route("/story_login")
def story_login():
    if LANGUAGE == "de":
        return flask.render_template(
            "secure/sm8_geschichte_anmeldung.html",
            flash="Validation succesfull!")
    else:
        return flask.render_template(
            "secure/sm8_story_login.html",
            flash="Validation succesfull!")


@app.route("/login", methods=["POST", "GET"])
def login():
    if flask.request.method == "POST":
        name = flask.request.form["name"]
        pwd = flask.request.form["pwd"]
        if name == users.get("sm_kd").username and pwd == users.get(
                "sm_kd").password:
            resp = flask.make_response(flask.redirect("/login_2fa"))
            return resp
        else:
            if LANGUAGE == "de":
                return flask.render_template(
                    "secure/sm9_anmeldung.html",
                    flash="Falsche Anmeldedaten!",
                    classes="fade show display",
                )
            else:
                return flask.render_template(
                    "secure/sm9_login.html",
                    flash="Wrong credentials!",
                    classes="fade show display",
                )
    else:
        if LANGUAGE == "de":
            return flask.render_template("secure/sm9_anmeldung.html")
        else:
            return flask.render_template("secure/sm9_login.html")


@app.route("/login_2fa", methods=["POST", "GET"])
def login_2fa():
    if flask.request.method == "POST":
        validation = flask.request.form["validation"]
        if validate_otp(users["sm_kd"].otp, validation):
            print("Succesfull validate qr")
            resp = flask.make_response(flask.redirect("/end"))
            return resp
        else:
            if LANGUAGE == "de":
                return flask.render_template(
                    "secure/sm10_anmeldung_2fa.html",
                    flash="Validierung fehlgeschlagen",
                    classes="fade show display",
                )
            else:
                return flask.render_template(
                    "secure/sm10_login_2fa.html",
                    flash="Validation failed",
                    classes="fade show display",
                )
    else:
        if LANGUAGE == "de":
            return flask.render_template(
                "secure/sm10_anmeldung_2fa.html",
                flash="Succesfully logged in!")
        else:
            return flask.render_template(
                "secure/sm10_login_2fa.html",
                flash="Succesfully logged in!")


@app.route("/end")
def end():
    if LANGUAGE == "de":
        return flask.render_template(
            "secure/sm11_geschichte_ende.html",
            flash="Validation succesfull!")
    else:
        return flask.render_template(
            "secure/sm11_story_end.html",
            flash="Validation succesfull!")


"""-------------------END SAFE MODE-------------------"""

if __name__ == "__main__":
    threading.Thread(target=run_flask_app).start()
    # webbrowser.open('http://127.0.0.1:5001/story_intro')
