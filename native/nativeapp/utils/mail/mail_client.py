#!/usr/bin/env python3

from contextlib import contextmanager
from email.message import EmailMessage
from email.mime.base import MIMEBase
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText
from email import encoders
from email import policy
from email.parser import BytesParser
from email.utils import format_datetime, parsedate_to_datetime

import imaplib
import smtplib
import logging
import datetime
import random
import pathlib
import yaml


class MailClient:
    def __init__(self, hostname, imap_port, smtp_port, username, password):
        self.hostname = hostname
        self.imap_port = imap_port
        self.smtp_port = smtp_port
        self.username = username
        self.password = password

    @contextmanager
    def imap_connect(self):
        imap_connection = None
        try:
            imap_connection = imaplib.IMAP4_SSL(
                    host=self.hostname, port=self.imap_port)
            imap_connection.login(user=self.username, password=self.password)
            yield imap_connection
        except Exception as e:
            logging.error(f"IMAP connection to \
                    \"{self.hostname}:{self.imap_port}\"failed: {e}")

        finally:
            if imap_connection is not None:
                imap_connection.close()
                imap_connection.logout()

    @contextmanager
    def smtp_connect(self):
        try:
            smtp_connection = smtplib.SMTP_SSL(
                    host=self.hostname, port=self.smtp_port)
            smtp_connection.login(self.username, self.password)
            yield smtp_connection
        except Exception as e:
            logging.error(f"SMTP connection to \
                    \"{self.hostname}:{self.smtp_port}\"failed: {e}")
        finally:
            smtp_connection.quit()

    def send_mail(self, message: EmailMessage):
        with self.smtp_connect() as session:
            try:
                # use the 'to' field as the true sender.
                # in the mail application message["from"] is shown
                sender = str(message["to"])
                logging.info("Sending mail from {} to {}"
                             .format(sender, message["to"]))
                session.sendmail(
                        sender, message["to"], message.as_bytes())
            except Exception as e:
                logging.error(e)

    def delete_mailbox(self, box_name="Inbox"):
        with self.imap_connect() as session:
            session.select(box_name)
            _, data = session.search(None, "ALL")
            for num in data[0].split():
                session.store(num, "+FLAGS", "\\Deleted")
            session.expunge()

    def get_message_from_file(self, email_file, random_date_interval=(1, 3)):
        email_file = pathlib.Path(email_file)
        logging.info("Sending mail file: {}".format(email_file))
        if not email_file.is_file():
            logging.error(f"\"{email_file}\" is not a file")
            return None

        if email_file.suffix == ".yml":
            try:
                with open(email_file, 'r',  encoding='utf-8') as file:
                    yml_data = yaml.safe_load(file)
            except Exception as e:
                logging.error(e)
                return None

            msg = MIMEMultipart()
            msg['Subject'] = yml_data["subject"]
            msg['From'] = "{} <{}>".format(
                    yml_data["from"]["display_name"],
                    yml_data["from"]["email"])
            msg['To'] = "{} <{}>".format(
                yml_data["to"]["display_name"],
                yml_data["to"]["email"])
            msg['Date'] = format_datetime(datetime.datetime.strptime(
                "2020-01-01 {}".format(str(yml_data["time"])),
                '%Y-%d-%m %H:%M'))
            msg.attach(MIMEText(yml_data["content"]))

            if "attachment" in yml_data:
                file_name = yml_data["attachment"]
                file_path = email_file.parent / file_name
                with open(file_path, "rb") as attachment_file:
                    part = MIMEBase("application", "octet-stream")
                    part.set_payload(attachment_file.read())
                encoders.encode_base64(part)
                # Add header as key/value pair to attachment part
                part.add_header(
                        "Content-Disposition",
                        f"attachment; filename={file_name}",
                        )
                msg.attach(part)

        elif email_file.suffix == ".txt":
            with open(email_file, 'rb') as fp:
                msg = BytesParser(policy=policy.default).parse(fp)

        # Substract "random_date_interval" days from today
        # we don't use random for crypto. no sec issue
        day_offset = random.randint(random_date_interval[0],  # nosec B311
                                    random_date_interval[1])
        date_obj = datetime.date.today() - \
            datetime.timedelta(days=day_offset)
        # replace msg header with new date and remain previous time
        date = parsedate_to_datetime(msg["Date"])
        date_str = date_obj.strftime(
            "%a, %d %b %Y {}".format(
               date.strftime("%H:%M")))
        msg.replace_header("date", date_str)

        return msg

    def send_mail_from_file(self, email_file):
        msg = self.get_message_from_file(email_file)
        self.send_mail(msg)
