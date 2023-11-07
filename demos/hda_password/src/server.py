import flask
import pathlib
import pyotp
import qrcode
import sys

HOST = "0.0.0.0"  # nosec No Issue in a Docker Container
LANGUAGE = "de"
random_id = pyotp.random_hex()
d_path = pathlib.Path(__file__).parent.absolute()
html_folder_path = pathlib.Path(d_path) / "templates"
static_folder_path = pathlib.Path(d_path) / "static"
websites_folder_path = pathlib.Path(html_folder_path) / "secure"
template_prefix = pathlib.Path("secure/")


app = flask.Flask(__name__)
localized_websites = []
users = {}


LOGIN_WEBSITE = 0
PASSWORD_REGISTRATION_WEBSITE = 1
TWO_FA_INTRO_WEBSITE = 2
TWO_FA_REGISTRATION_WEBISTE = 3
LOGIN_INFO_WEBISTE = 4
PASSWORD_LOGIN_WEBSITE = 5
TWO_FA_LOGIN_WEBSITE = 6
SUCCESS_WEBSITE = 7


"""-------------------UTILS-------------------"""


class User:
    def __init__(self, username, password, otp):
        self.username = username
        self.password = password
        self.otp = otp


def validate_otp(otp, temp_code):
    totp = pyotp.TOTP(otp)
    print(totp.now())
    if totp.verify(otp=temp_code, valid_window=10):
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
    print("- Start Server")
    app.config.from_pyfile("config.py", silent=True)
    app.run(host=HOST, port="5001", threaded=True)


def create_qr(user_name, otp):
    url = pyotp.totp.TOTP(otp).provisioning_uri(
        name=user_name, issuer_name="Nimbus 2FA Service"
    )
    qr = qrcode.QRCode(
        version=1,
        error_correction=qrcode.constants.ERROR_CORRECT_H,
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
    return flask.send_file(str(file_path))


@app.route("/")
@app.route("/story_intro")
def story_intro_sm():
    return flask.render_template(str(pathlib.Path(template_prefix) /
                                 localized_websites[LOGIN_WEBSITE].name))


@app.route("/register_account_services", methods=["POST", "GET"])
def registration_kontodienste_sm():
    if flask.request.method == "POST":
        user_name = flask.request.form["name"]
        user_password = flask.request.form["password"]
        resp = flask.make_response(flask.redirect(
            "/init_2fa_account_services"))
        user = create_user(user_name, user_password, "sm_kd")
        qr_code = create_qr(user_name, user.otp)
        qr_code.save(pathlib.Path(static_folder_path) / "qrcode3.jpg")
        return resp
    else:
        return flask.render_template(str(pathlib.Path(template_prefix) /
                                     localized_websites
                                     [PASSWORD_REGISTRATION_WEBSITE]
                                     .name))


@app.route("/story_2fa")
def story_2fa_sm():
    return flask.render_template(str(pathlib.Path(template_prefix) /
                                 localized_websites
                                 [TWO_FA_INTRO_WEBSITE].name),
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
            return flask.render_template(str(pathlib.Path(template_prefix) /
                                         localized_websites
                                         [TWO_FA_REGISTRATION_WEBISTE].name),
                                         flash="validation failed!",
                                         classes="fade show display",)
    else:
        return flask.render_template(str(pathlib.Path(template_prefix) /
                                     localized_websites
                                     [TWO_FA_REGISTRATION_WEBISTE].name))


@app.route("/story_login")
def story_login():
    return flask.render_template(str(pathlib.Path(template_prefix) /
                                 localized_websites
                                 [LOGIN_INFO_WEBISTE].name),
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
            return flask.render_template(str(pathlib.Path(template_prefix) /
                                         localized_websites
                                         [PASSWORD_LOGIN_WEBSITE].name),
                                         flash="Wrong credentials!",
                                         classes="fade show display",)
    else:
        return flask.render_template(str(pathlib.Path(template_prefix) /
                                     localized_websites
                                     [PASSWORD_LOGIN_WEBSITE].name))


@app.route("/login_2fa", methods=["POST", "GET"])
def login_2fa():
    if flask.request.method == "POST":
        validation = flask.request.form["validation"]
        if validate_otp(users["sm_kd"].otp, validation):
            print("Succesfull validate qr")
            resp = flask.make_response(flask.redirect("/end"))
            return resp
        else:
            return flask.render_template(str(pathlib.Path(template_prefix) /
                                         localized_websites
                                         [TWO_FA_LOGIN_WEBSITE].name),
                                         flash="Validation failed",
                                         classes="fade show display")
    else:
        return flask.render_template(str(pathlib.Path(template_prefix) /
                                     localized_websites
                                     [TWO_FA_LOGIN_WEBSITE].name),
                                     flash="Succesfully logged in!")


@app.route("/end")
def end():
    return flask.render_template(str(pathlib.Path(template_prefix) /
                                 localized_websites[SUCCESS_WEBSITE].name),
                                 flash="Validation succesfull!")


"""-------------------END SAFE MODE-------------------"""

if __name__ == "__main__":
    LANGUAGE = sys.argv[1]
    try:
        localized_websites_folder_path = pathlib.Path(websites_folder_path) /\
                                         LANGUAGE
        if localized_websites_folder_path.exists():
            template_prefix = pathlib.Path("secure/") / LANGUAGE
        else:
            localized_websites_folder_path = pathlib.Path(
                                             websites_folder_path) / "de"
            template_prefix = pathlib.Path("secure/de/")
        for entry in sorted(localized_websites_folder_path.iterdir()):
            # check if it a file
            if entry.is_file():
                localized_websites.append(entry)
    except Exception as e:
        print(e)
    run_flask_app()
    # webbrowser.open('http://127.0.0.1:5001/story_intro')
