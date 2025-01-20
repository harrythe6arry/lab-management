from urllib import request

from flask import Flask, render_template, redirect, url_for

app = Flask(__name__)


@app.route('/')
def hello_world():  # put application's code here
    return 'Hello World!'


if __name__ == '__main__':
    app.run()
@app.route('/login')
def login():
    return render_template('login.html')


