import qrcode


class Otp:
    def __init__(self):
        print("")

    def create_qr(self, userid, otp):
        qr = qrcode.QRCode(
            version=1,
            error_correction=qrcode.constants.ERROR_CORRECT_L,
            box_size=10,
            border=4,
        )
        qr.add_data(otp)
        qr.make(fit=True)
        img = qr.make_image(fill_color="black", back_color="white")
        img.save(userid + "-qrcode.jpg")
        return img
