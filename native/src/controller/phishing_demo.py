import flask

from native.src.service import phishing_demo

phishing_demo_service = phishing_demo.PhishingDemo()

phishing_demo = flask.Blueprint("phishingdemo", __name__,
                                url_prefix="/phishingdemo/")


@phishing_demo.route("/deletemailbox", methods=["POST", "GET"])
def delete_mailbox():
    return phishing_demo_service.delete_mailbox()


@phishing_demo.route("/sendmails", methods=["POST", "GET"])
def send_mail_files():
    return phishing_demo_service.send_mail_files()


# @phishing_demo.route("/use_secure_client/<use_secured_client>",
#                      methods=["POST", "GET"])
# def change_client_profile():
#     if use_secured_client.lower() == "true":
#         return phishing_demo_service.change_client_profile(
#             use_secured_client=True)
#     else:
#         return phishing_demo_service.change_client_profile(
#             use_secured_client=False)
