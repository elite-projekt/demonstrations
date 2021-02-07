import smtplib
import imaplib
import glob
import ssl
import email
import os
import re
import random
from datetime import date, datetime, timedelta
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart

default_email_server = "141.100.70.56" #online vm server
# default_email_server = "192.168.178.115" #local server

default_email_account = "max.mustermann@mpseinternational.com"
default_email_account_password = "123"

secure_server_smtp_port = 25
secure_server_imap_port = 143
unsecure_server_smtp_port = 26
unsecure_server_imap_port = 144

# sender_email = "test2@example.org" #"max.mustermann@mpseinternational.com" #test2@example.org
# receiver_email = "max.mustermann@mpseinternational.com"
# email_password = "123"

# email_client_config_location = r"C:\Users\Jan\AppData\Roaming\Thunderbird\Profiles\sldrcrlj.MPSE\prefs.js"
email_client_config_location = os.getenv('APPDATA') + r"\Thunderbird\Profiles\sldrcrlj.MPSE\prefs.js"
email_files_location = "emails\\eng\\"

email_text_placeholder = """\
Placeholder"""
email_html_placeholder = """\
<html>
    <body>
        <p>
            <a href="http://www.example.org">Placeholder</a> 
        </p>
    </body>
</html>
"""


def create_mail(subject="Placehholder_Subject",
                sender="Placehholder_Sender",
                recipient="Placehholder_Recipient",
                date="Fri, 01 Jan 2021 00:00:00 +0100",
                text=email_text_placeholder,
                html=email_html_placeholder):
    mail = MIMEMultipart("alternative")
    mail["Subject"] = subject
    mail["From"] = sender
    mail["To"] = recipient
    mail["Date"] = date

    # Turn these into plain/html MIMEText objects
    f = open("email_html.html", "r")
    html_from_file = f.read()
    f.close()
    part1 = MIMEText(text, "plain", "utf-8")
    part2 = MIMEText(html_from_file, "html", "utf-8")

    # Add HTML/plain-text parts to MIMEMultipart message
    # The email client will try to render the last part first
    mail.attach(part1)
    mail.attach(part2)
    return mail


# delete all mails for a specified email account
def delete_mailbox(local_imap_port=secure_server_imap_port,
                   local_email_server=default_email_server,
                   local_email_account=default_email_account,
                   local_email_account_password=default_email_account_password):
    box = imaplib.IMAP4(local_email_server, local_imap_port)
    box.login(local_email_account, local_email_account_password)
    box.select('Inbox')
    typ, data = box.search(None, 'ALL')
    for num in data[0].split():
        box.store(num, '+FLAGS', '\\Deleted')
    box.expunge()
    box.close()
    box.logout()


# Ports to be used: secure_server_smtp_port or unsecure_server_smtp_port
def send_mail(sender, password, port, recipient, message, local_server=default_email_server):
    # Try to log in to server and send email
    server = smtplib.SMTP(local_server, port)
    try:
        # server.auth_plain()
        server.login(sender, password)
        # server.auth_plain()
        print("Sending mail from " + sender + " to " + recipient)
        server.sendmail(sender, recipient, message)
    except Exception as e:
        # Print any error messages to stdout
        print(e)
    server.close()


def send_multiple_mails_from_files(local_password, port, local_server=default_email_server):
    for file in glob.glob(email_files_location + "*.txt"):
        email_file = open(file, "r")
        email_text = email_file.read()
        email_mime = email.message_from_string(email_text)

        # Extract the sender of the email
        # If the form '"name" <name@domain>' is used the raw address is extracted
        local_sender = email_mime["From"]
        local_left_bracket = local_sender.find("<")
        local_right_bracket = local_sender.find(">")
        if -1 < local_left_bracket < local_right_bracket:
            local_sender = re.split('[<>]', local_sender)[1]

        # Extract the "Sent" time from the email source
        email_date = email_mime["Date"]
        email_time = datetime.strptime(email_date, "%a, %d %b %Y %H:%M:%S +0100")

        # Substract one day so the sent date is yesterday
        date_object = date.today() - timedelta(days=1)

        # Email date format "Fri, 01 Jan 2021 00:00:00 +0100"
        email_date = date_object.strftime("%a, %d %b %Y " + email_time.strftime("%H:%M:%S") + " +0100")

        email_mime.replace_header("Date", email_date)
        email_text = email_mime.as_string()

        send_mail(local_sender, local_password, port, email_mime["To"], email_text, local_server)
        email_file.close()


def change_client_profile(use_secured_client=True, change_ports=False):
    """
    Changes the client configuration between a more secure and a less secure configuration
    :param use_secured_client: Which client configuration to use
    :param change_ports: Do we want to change ports in the config?
    :return:
    """
    with open(email_client_config_location, "r") as f:
        f_lines = f.readlines()

        # only touch port configuration if we really want to (multiple email servers with
        # different ports are not in scope of the WS20/21
        if change_ports:
            i = 0
            imap_port_set = False
            smtp_port_set = False
            while i < len(f_lines):
                if "mail.server.server1.port" in f_lines[i] and use_secured_client:
                    f_lines[i] = f_lines[i].replace(str(unsecure_server_imap_port), str(secure_server_imap_port))
                    imap_port_set = True
                elif "mail.server.server1.port" in f_lines[i] and  not use_secured_client:
                    f_lines[i] = f_lines[i].replace(str(secure_server_imap_port), str(unsecure_server_imap_port))
                    imap_port_set = True
                elif "mail.smtpserver.smtp1.port" in f_lines[i] and use_secured_client:
                    f_lines[i] = f_lines[i].replace(str(unsecure_server_smtp_port), str(secure_server_smtp_port))
                    smtp_port_set = True
                elif "mail.smtpserver.smtp1.port" in f_lines[i] and not use_secured_client:
                    f_lines[i] = f_lines[i].replace(str(secure_server_smtp_port), str(unsecure_server_smtp_port))
                    smtp_port_set = True
                i += 1

            if not imap_port_set:
                if use_secured_client:
                    f_lines.append("user_pref(\"mail.server.server1.port\", " + str(secure_server_imap_port) + ");\n")
                elif not use_secured_client:
                    f_lines.append("user_pref(\"mail.server.server1.port\", " + str(unsecure_server_imap_port) + ");\n")

            if not smtp_port_set:
                if use_secured_client:
                    f_lines.append("user_pref(\"mail.server.server1.port\", " + str(secure_server_smtp_port) + ");\n")
                elif not use_secured_client:
                    f_lines.append("user_pref(\"mail.server.server1.port\", " + str(unsecure_server_smtp_port) + ");\n")

        # user_pref("mail.phishing.detection.enabled", false);
        # user_pref("mailnews.message_display.disable_remote_image", false);
        i = 0
        phishing_detection_set = False
        remote_image_set = False
        while i < len(f_lines):
            if "mail.phishing.detection.enabled" in f_lines[i] and use_secured_client:
                f_lines[i] = f_lines[i].replace("false", "true")
                phishing_detection_set = True
            elif "mail.phishing.detection.enabled" in f_lines[i] and not use_secured_client:
                f_lines[i] = f_lines[i].replace("true", "false")
                phishing_detection_set = True
            elif "mailnews.message_display.disable_remote_image" in f_lines[i] and use_secured_client:
                f_lines[i] = f_lines[i].replace("false", "true")
                remote_image_set = True
            elif "mailnews.message_display.disable_remote_image" in f_lines[i] and not use_secured_client:
                f_lines[i] = f_lines[i].replace("true", "false")
                remote_image_set = True
            i += 1

        if not phishing_detection_set:
            if use_secured_client:
                f_lines.append("user_pref(\"mail.phishing.detection.enabled\", true);\n")
            elif not use_secured_client:
                f_lines.append("user_pref(\"mail.phishing.detection.enabled\", false);\n")

        if not remote_image_set:
            if use_secured_client:
                f_lines.append("user_pref(\"mailnews.message_display.disable_remote_image\", true);\n")
            elif not use_secured_client:
                f_lines.append("user_pref(\"mailnews.message_display.disable_remote_image\", false);\n")

    with open(email_client_config_location, "w") as f:
        f.writelines(f_lines)
    return "Set client configuration to secure" if use_secured_client else "Set client configuration to unsecure"


#print(change_client_profile(use_secured_client=True))

# f = open("email.txt", "w")
# a = create_mail(subject="Test2", sender=default_email_account, recipient="test2@example.org")
# f.write(a.as_string()) # create_mail(subject="Test2", sender=sender_email, recipient="test2@example.org").as_string())
# f.close()

delete_mailbox()
send_multiple_mails_from_files(default_email_account_password, secure_server_smtp_port)

# f = open("email.txt", "r")
# mail_message = f.read()
# send_mail(sender="test2@example.org", password=email_password, port=secure_server_smtp_port, recipient=receiver_email, message=mail_message, server=email_server)
