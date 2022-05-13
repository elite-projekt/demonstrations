import unittest

from nativeapp.utils.mail import mail_client

from email.utils import parsedate_to_datetime
from datetime import datetime
import pathlib

SCRIPT_DIR = pathlib.Path(__file__).parent


class TestMail(unittest.TestCase):

    def _test_msg(self, msg):
        self.assertEqual(
                str(msg["to"]),
                "Max Mustermann <max.mustermann@mpseinternational.com>")
        self.assertEqual(
                str(msg["from"]),
                "Christina Sauer <christina.sauer@mpseinternational.com>")
        self.assertEqual(
                msg["subject"],
                "Save the date: Farewell party for Harald")
        mail_date = parsedate_to_datetime(msg["Date"])
        test_date = datetime.today().replace(
                hour=12, minute=31, second=0, microsecond=0)
        self.assertEqual(mail_date, test_date)
        mail_content = """Content-Type: text/plain; charset="utf-8"
MIME-Version: 1.0
Content-Transfer-Encoding: base64

SGVsbG8gZXZlcnlvbmUsCgp3ZSBzdGlsbCBuZWVkIHRvIGZpbmQgYSBkYXRlIHRvIHNheSBnb29k
YnllIHRvIEhhcmFsZC4gSSBoYXZlIGNyZWF0ZWQgYQpkb29kbGUgYW5kIGl0IHdvdWxkIGJlIG5p
Y2UgaWYgZXZlcnlvbmUgZW50ZXJzIGhpcyBmcmVlIGRhdGVzLgoKSGVyZSBpcyB0aGUgbGluazoK
aHR0cHM6Ly9kb29kbGUuY29tL3BvbGwvZTRjejJ4bmU2eXFkeGJ4ZD91dG1fc291cmNlPXBvbGwm
dXRtX21lZGl1bT1saW5rCgrDpMOkbMO2w7zDnwpCZXN0IFJlZ2FyZHMKQ2hyaXN0aW5hCg==
"""
        self.assertEqual(len(msg.get_payload()), 2)
        self.assertEqual(str(msg.get_payload()[0]), mail_content)

        mail_attachment = """Content-Type: application/octet-stream
MIME-Version: 1.0
Content-Transfer-Encoding: base64
Content-Disposition: attachment; filename=test_data

t3b5XA6olJBxEJtA81SULpGpJuCUHTSiZteM93iQCATMGX6RIQ9LS7XHJCLE1tK39HxcpO/N1+kr
Eh7Bx1gP0mMH260uDnVG3Yu1O/5KoICuroQz5QQ3T3e0Wgyuxg5mdKvk3aJjbyqyE/pqoOeApa+l
RmvbZbwVXelgQppqZ4X+f6TPriQNESKDsJs5F1E9NrrqZIqfdzWRl9xOIvgfnEvDqnxtgwy/O8u2
4dzXKZVx37NZ6+EeQ0Kd4zlEkihUpPTx3E4KCWL+bR/usxVS8vMn8afVKiNu4XFVzWNPV8GYTXVg
lyoA4IHqdGFNK28eGhVmX8SE7iGHwhO+gKBPnYA1nd7WDO68TqTGUDAQHpJRrtWi9iXjgegflMkm
UHRo2ejBQvRpvlE+1bT1lEQhAKzleKuZ6gKup4lF2W/eepVZ8VR4yLk+63Nvf3d9GFySMN/vG+ez
a/+dTmPP9S6ay0Zr1Wl/A9eSD6R7eqQxVH7if4jx3DemBPEy6Biq1PzKtfm9waVvQ5i/IPdz9kV6
OzcqQzg/HHU1jNsbGmJ76rBQaxUQktKIJK+Ov5+vnxY4a1NJP1H6qfF1qUjJoGVYcmp60id1I2kh
mzSkRroPpBKhIqIsAAKpoTr/4z52JPppcv8U/g9e+NG+JRbOEPYqy4Qi86DXdN6d/lvOExlgUJU=
"""
        self.assertEqual(str(msg.get_payload()[1]), mail_attachment)

    def test_mail_yaml(self):
        email_client = mail_client.MailClient("host", 123, 123, "user", "pass")
        m = email_client.get_message_from_file(SCRIPT_DIR / "test_mail.yml",
                                               (0, 0))
        self._test_msg(m)

    def test_mail_txt(self):
        email_client = mail_client.MailClient("host", 123, 123, "user", "pass")
        m = email_client.get_message_from_file(SCRIPT_DIR / "test_mail.txt",
                                               (0, 0))
        self._test_msg(m)


if __name__ == "__main__":
    unittest.main()
