from flask import Flask, request, send_from_directory, send_file
# set the project root directory as the static folder, you can set others.
app = Flask(__name__, static_url_path='')
app.config.from_pyfile('config.py', silent=True)
app._static_folder = ""

@app.route('/neuerAntrag')
def root():
    return send_file('E:\Studium\Semester 3\MPSE Experiencing Cyber Security\git\Phishing Demo\Landing Pages\html\corona.html')
    #return app.send_static_file('antrag.html')

if __name__ == "__main__":
    app.run(host='127.0.0.1', port=443,
            ssl_context=(r'E:\Studium\Semester 3\MPSE Experiencing Cyber Security\git\Phishing Demo\Landing Pages\server.crt',
                         r'E:\Studium\Semester 3\MPSE Experiencing Cyber Security\git\Phishing Demo\Landing Pages\server.key'))
