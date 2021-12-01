import os
import threading

import flask
import pyotp
import qrcode

HOST = "0.0.0.0"
random_id = pyotp.random_hex()
d_path = os.path.abspath(os.path.dirname(__file__))
html_folder_path = os.path.join(d_path, "template")
static_folder_path = os.path.join(d_path, "static")

app1 = flask.Flask(__name__)
app2 = flask.Flask(__name__)
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


def run_flask_app_unsave():
    """
    Creates Flask server 1.
    :return:
    """
    print("- Start Server 1")
    app1.config.from_pyfile("config.py", silent=True)
    app1.run(host=HOST, port=5000, threaded=True)


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


def run_flask_app_save():
    """
    Creates Flask server 2.
    :return:
    """
    print("- Start Server 2")
    app2.config.from_pyfile("config.py", silent=True)
    app2.run(host=HOST, port=5001, threaded=True)


def create_qr(user_name, otp):
    url = pyotp.totp.TOTP(otp).provisioning_uri(
        name=user_name, issuer_name="Secure App"
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


"""-------------------BEGINN UNSAFE MODE-------------------"""


@app1.route("/story_intro")
def story_intro_um():
    return flask.render_template("um1_story_intro.html")


@app1.route("/registration_kontodienste", methods=["POST", "GET"])
def registration_kontodienste_um():
    if flask.request.method == "POST":
        user_name = flask.request.form["name"]
        user_password = flask.request.form["pwd"]
        resp \
            = flask.make_response(flask.redirect("/story_second_registration"))
        create_user(user_name, user_password, "um_kd")
        return resp
    else:
        return flask.render_template("um2_registration_kontodienste.html")


@app1.route("/story_second_registration")
def story_second_registration_um():
    return flask.render_template(
        "um3_story_second_registration.html", flash="Registration succesfull!"
    )


@app1.route("/registration_webdienste", methods=["POST", "GET"])
def registration_webdienste_um():
    if flask.request.method == "POST":

        user_name = flask.request.form["name"]
        user_password = flask.request.form["pwd"]
        resp = flask.make_response(flask.redirect("/story_login"))
        create_user(user_name, user_password, "um_wd")
        return resp
    else:
        return flask.render_template(
            "um4_registration_webdienste.html",
            username=users.get("um_kd").username
        )


@app1.route("/story_login")
def story_login_um():
    return flask.render_template("um5_story_login.html",
                                 flash="Registration succesfull!")


@app1.route("/login", methods=["POST", "GET"])
def login_um():
    if flask.request.method == "POST":
        name = flask.request.form["name"]
        pwd = flask.request.form["pwd"]
        if name == users.get("um_kd").username and pwd == users.get(
                "um_kd").password:
            resp = flask.make_response(flask.redirect("/end"))
            return resp
        else:
            return flask.render_template(
                "um6_login.html",
                flash="Wrong credentials!",
                classes="fade show display",
            )
    else:
        return flask.render_template("um6_login.html")


@app1.route("/end")
def end_um():
    return flask.render_template("um7_story_end.html",
                                 flash="login sucessfull!")


"""-------------------END UNSAFE MODE-------------------"""

"""-------------------BEGINN SAFE MODE-------------------"""


@app2.route("/story_intro")
def story_intro_sm():
    return flask.render_template("sm1_story_intro.html")


@app2.route("/registration_kontodienste", methods=["POST", "GET"])
def registration_kontodienste_sm():
    if flask.request.method == "POST":

        user_name = flask.request.form["name"]
        user_password = flask.request.form["password"]
        resp = flask.make_response(flask.redirect("/story_2fa"))
        user = create_user(user_name, user_password, "sm_kd")
        qr_code = create_qr(user_name + "_qr_account_services", user.otp)
        qr_code.save(static_folder_path + "/" + "qrcode1.jpg")
        return resp
    else:
        return flask.render_template("sm2_registration_kontodienste.html")


@app2.route("/story_2fa")
def story_2fa_sm():
    return flask.render_template("sm3_story_2fa.html",
                                 flash="Registration succesfull!")


@app2.route("/initial_2fa_kontodienste", methods=["POST", "GET"])
def initial_2fa_kontodienste_sm():
    if flask.request.method == "POST":
        validation = flask.request.form["validation"]
        if validate_otp(users.get("sm_kd").otp, validation):
            resp = flask.make_response(
                flask.redirect("/story_second_registration"))
            print("Succesfull validate qr")
            return resp
        else:
            print("wrong validation")
            return flask.render_template(
                "sm4_initial_2fa_kontodienste.html", flash="validation failed!"
            )
    else:
        return flask.render_template("sm4_initial_2fa_kontodienste.html")


@app2.route("/story_second_registration")
def story_second_registration_sm():
    return flask.render_template(
        "sm5_story_second_registration.html", flash="Validation succesfull!"
    )


@app2.route("/registration_webdienste", methods=["POST", "GET"])
def registration_webdienste_sm():
    if flask.request.method == "POST":

        user_name = flask.request.form["name"]
        user_password = flask.request.form["password"]
        if user_password == users.get("sm_kd").password:
            return flask.render_template(
                "sm6_registration_webdienste.html",
                flash="you cannot use the same password as for the "
                      "Kontodienste ",
                classes="fade show display",
            )
        resp = flask.make_response(flask.redirect("/initial_2fa_webdienste"))
        user = create_user(user_name, user_password, "sm_wd")
        qr_code = create_qr(user_name + "_qr_web_services", user.otp)
        qr_code.save(static_folder_path + "/" + "qrcode2.jpg")
        return resp
    else:
        return flask.render_template(
            "sm6_registration_webdienste.html",
            username=users.get("sm_kd").username
        )


@app2.route("/initial_2fa_webdienste", methods=["POST", "GET"])
def initial_2fa_webdienste():
    if flask.request.method == "POST":
        validation = flask.request.form["validation"]
        if validate_otp(users["sm_wd"].otp, validation):
            resp = flask.make_response(flask.redirect("/story_login"))
            print("Succesfull validate qr")
            return resp
        else:
            print("wrong validation")
            return flask.render_template(
                "sm7_initial_2fa_webdienste.html", flash="Validation failed!"
            )
    else:
        return flask.render_template(
            "sm7_initial_2fa_webdienste.html", flash="Registration succesfull!"
        )


@app2.route("/story_login")
def story_login():
    return flask.render_template("sm8_story_login.html",
                                 flash="Validation succesfull!")


@app2.route("/login", methods=["POST", "GET"])
def login():
    if flask.request.method == "POST":
        name = flask.request.form["name"]
        pwd = flask.request.form["pwd"]
        if name == users.get("sm_kd").username and pwd == users.get(
                "sm_kd").password:
            resp = flask.make_response(flask.redirect("/login_2fa"))
            return resp
        else:
            return flask.render_template(
                "sm9_login.html",
                flash="Wrong credentials!",
                classes="fade show display",
            )
    else:
        return flask.render_template("sm9_login.html")


@app2.route("/login_2fa", methods=["POST", "GET"])
def login_2fa():
    if flask.request.method == "POST":
        validation = flask.request.form["validation"]
        if validate_otp(users["sm_kd"].otp, validation):
            print("Succesfull validate qr")
            resp = flask.make_response(flask.redirect("/end"))
            return resp
        else:
            return flask.render_template("sm10_login_2fa.html",
                                         flash="Validation failed")
    else:
        return flask.render_template("sm10_login_2fa.html",
                                     flash="Succesfully logged in!")


@app2.route("/end")
def end():
    return flask.render_template("sm11_story_end.html",
                                 flash="Validation succesfull!")


"""-------------------END SAFE MODE-------------------"""

if __name__ == "__main__":
    threading.Thread(target=run_flask_app_unsave).start()
    threading.Thread(target=run_flask_app_save).start()
    # webbrowser.open('http://127.0.0.1:5001/story_intro')
