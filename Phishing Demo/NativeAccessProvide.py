import smtplib
import imaplib
import ssl
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart

email_server = "192.168.56.101"
secure_server_smtp_port = 25
secure_server_imap_port = 143
unsecure_server_smtp_port = 26
unsecure_server_imap_port = 144
sender_email = "max.mustermann@mpseinternational.com" #test2@example.org
receiver_email = "max.mustermann@mpseinternational.com"
password = "123"

email_client_location = r"C:\Users\Jan\AppData\Roaming\Thunderbird\Profiles\sldrcrlj.MPSE\prefs.js"

def create_mail():
    message = MIMEMultipart("alternative")
    message["Subject"] = "test"
    message["From"] = sender_email
    message["To"] = receiver_email
    message["Date"] = "Wed, 16 Dec 2020 00:24:26 +0100"


    # Create the plain-text and HTML version of your message
    text = """\
    Einfacher Nachrichtentext"""
    html = """\
    <html>
      <body>
        <p>Hi,<br>
           HTML<br>
           <a href="http://www.mpseinternational.com">www.mpseinternational.com</a> 
        </p>
      </body>
    </html>
    """

    # Turn these into plain/html MIMEText objects
    part1 = MIMEText(text, "plain")
    part2 = MIMEText(html, "html")

    # Add HTML/plain-text parts to MIMEMultipart message
    # The email client will try to render the last part first
    message.attach(part1)
    message.attach(part2)
    return message


def send_mail(message):
    # Try to log in to server and send email
    server = smtplib.SMTP(email_server, secure_server_smtp_port)
    try:
        # server.auth_plain()
        server.login(sender_email, password)
        # TODO: Send email here
        # server.auth_plain()
        server.sendmail(sender_email, receiver_email, message.as_string())
    except Exception as e:
        # Print any error messages to stdout
        print(e)
    server.close()


def delete_mailbox():
    box = imaplib.IMAP4(email_server, secure_server_imap_port)
    box.login(sender_email, password)
    box.select('Inbox')
    typ, data = box.search(None, 'ALL')
    for num in data[0].split():
        print(num)
        box.store(num, '+FLAGS', '\\Deleted')
    box.expunge()
    box.close()
    box.logout()


def change_client_profile(use_secured_client=True):
    with open(email_client_location, "r") as f:
        f_lines = f.readlines()
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
                f_lines.append("user_pref(\"mail.server.server1.port\", " + str(secure_server_imap_port) + r");")
            elif not use_secured_client:
                f_lines.append("user_pref(\"mail.server.server1.port\", " + str(unsecure_server_imap_port) + r");")

        if not smtp_port_set:
            if use_secured_client:
                f_lines.append("user_pref(\"mail.server.server1.port\", " + str(secure_server_smtp_port) + r");")
            elif not use_secured_client:
                f_lines.append("user_pref(\"mail.server.server1.port\", " + str(unsecure_server_smtp_port) + r");")

    with open(email_client_location, "w") as f:
        f.writelines(f_lines)
    return


change_client_profile(use_secured_client=True)
mail_message = create_mail()
send_mail(mail_message)
# delete_mailbox()
