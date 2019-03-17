from flask import render_template, Flask, request

app = Flask(__name__)


@app.route('/')
@app.route('/main')
def main():
    return render_template('app/main.html')


@app.route('/login', methods=['POST', 'GET'])
def login():
    if request.method == 'POST':
        print(1)
        print(request.form['Логин'])
    return render_template('app/login.html')


@app.route('/editor')
def editor():
    return render_template('app/editor.html')


app.run('127.0.0.1', 8080)
