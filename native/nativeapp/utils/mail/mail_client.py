#!/usr/bin/env python3

# SPDX-License-Identifier: AGPL-3.0-only

from contextlib import contextmanager
from email.message import EmailMessage
from email.mime.base import MIMEBase
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText
from email import encoders
from email import policy
from email.parser import BytesParser
from email.utils import format_datetime, parsedate_to_datetime, formataddr

import imaplib
import smtplib
import logging
import datetime
import random
import pathlib
import time
import yaml


class MailClient:
    """
    IMAP and SMTP client
    """
    def __init__(self, hostname, imap_port, smtp_port, username, password):
        self.hostname = hostname
        self.imap_port = imap_port
        self.smtp_port = smtp_port
        self.username = username
        self.password = password

    def wait_for_imap_server(self, max_timeout_s: float = 10) -> bool:
        """
        Tests if the imap server is reachable.
        Blocks until the server is reachable or [max_timeout_s] is reached
        """
        start_time = time.time()
        logging.info("Waiting for IMAP server")
        while time.time() - start_time < max_timeout_s:
            with self.imap_connect(False) as session:
                if session:
                    logging.info(f"IMAP Server online after \
                        {time.time() - start_time} seconds")
                    return True
        logging.info("Giving up after reaching timeout")
        return False

    def wait_for_smtp_server(self, max_timeout_s: float = 10) -> bool:
        """
        Blocks until [max_timeout_s] or the server is online
        """
        start_time = time.time()
        logging.info("Waiting for SMTP server")
        while time.time() - start_time < max_timeout_s:
            with self.smtp_connect(False) as session:
                if session:
                    logging.info(f"SMTP Server online after \
                        {time.time() - start_time} seconds")
                    return True
        logging.info("Giving up after reaching timeout")
        return False

    @contextmanager
    def imap_connect(self, show_error=True):
        """
        Connect to the imap server
        :param bool show_error: If false no errors are printes
        """
        imap_connection = None
        try:
            imap_connection = imaplib.IMAP4_SSL(
                    host=self.hostname, port=self.imap_port)
            imap_connection.login(user=self.username, password=self.password)
            imap_connection.select()
            yield imap_connection
        except Exception as e:
            if show_error:
                logging.error(f"IMAP connection to \
                        \"{self.hostname}:{self.imap_port}\"failed: {e}")
            yield None

        finally:
            if imap_connection is not None:
                imap_connection.close()
                imap_connection.logout()

    @contextmanager
    def smtp_connect(self, show_error=True):
        """
        Connect to the smtp server
        :param bool show_error: If false no errors are printes
        """
        smtp_connection = None
        try:
            smtp_connection = smtplib.SMTP_SSL(
                    host=self.hostname, port=self.smtp_port)
            smtp_connection.login(self.username, self.password)
            yield smtp_connection
        except Exception as e:
            if show_error:
                logging.error(f"SMTP connection to \
                        \"{self.hostname}:{self.smtp_port}\"failed: {e}")
            yield None
        finally:
            if smtp_connection is not None:
                smtp_connection.quit()

    def send_mail(self, message: EmailMessage, target_addr: str = None):
        with self.smtp_connect() as session:
            try:
                # use the 'to' field as the true sender.
                # in the mail application message["from"] is shown
                sender = str(message["to"])
                logging.info("Sending mail from {} to {}"
                             .format(sender, message["to"]))
                if target_addr is None:
                    target_addr = message["to"]
                session.sendmail(
                        sender, target_addr, message.as_bytes())
            except Exception as e:
                logging.error(e)

    def delete_mailbox(self, box_name="Inbox"):
        with self.imap_connect() as session:
            session.select(box_name)
            _, data = session.search(None, "ALL")
            for num in data[0].split():
                session.store(num, "+FLAGS", "\\Deleted")
            session.expunge()

    # TODO: remove duplicate code
    # (I don't want to risk breaking stuff right now)
    def get_message(self, subject, from_name, from_mail, to_name, to_mail,
                    content, attachment_path=None, _=None,
                    random_date_interval=(0, 0)):
        if _ is None:
            def identity(x):
                return x
            _ = identity

        attachment_path = pathlib.Path(attachment_path)
        msg = MIMEMultipart()
        msg['Subject'] = _(subject)
        msg['From'] = formataddr((_(from_name), _(from_mail)))
        msg['To'] = formataddr((_(to_name), _(to_mail)))
        msg["Date"] = format_datetime(
                datetime.datetime.now())
        msg.attach(MIMEText(_(content)))

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

        if attachment_path is not None:
            with open(attachment_path, "rb") as attachment_file:
                part = MIMEBase("application", "octet-stream")
                part.set_payload(attachment_file.read())
            encoders.encode_base64(part)
            # Add header as key/value pair to attachment part
            part.add_header(
                    "Content-Disposition",
                    f"attachment; filename={attachment_path.name}",
                    )
            msg.attach(part)
        return msg

    def get_message_from_file(self,
                              email_file,
                              random_date_interval=(1, 3),
                              _=None):
        """
        This constructs a mail from the given file


        :param email_file: The file which contains the content of the mail.
        This can be a .yml or .txt file
        :param random_date_interval: Changes the sending day randomly by the
        given offset
        :param _: A locale object to translate string in the given file.
        Pass None to do nothing
        """
        if _ is None:
            def identity(x):
                return x
            _ = identity
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
            msg['Subject'] = _(yml_data["subject"])
            msg['From'] = formataddr((yml_data["from"]["display_name"],
                                      yml_data["from"]["email"]))
            msg['To'] = formataddr((yml_data["to"]["display_name"],
                                    yml_data["to"]["email"]))
            if "time" in yml_data:
                msg['Date'] = format_datetime(datetime.datetime.strptime(
                    "2020-01-01 {}".format(str(yml_data["time"])),
                    '%Y-%d-%m %H:%M'))
            else:
                msg["Date"] = format_datetime(datetime.datetime.now())
            msg.attach(MIMEText(_(yml_data["content"])))

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
        else:
            raise NotImplementedError(f"We don't support {email_file.suffix} files as input yet!") # noqa: 501

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

    def send_mail_from_file(self, email_file, random_date_interval=(1, 3),
                            _=None):
        msg = self.get_message_from_file(email_file, random_date_interval, _)
        self.send_mail(msg)
