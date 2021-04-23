from config import app  # , login_manager
from flask import render_template
from models import *
from forms import *


@app.route('/', methods=['GET', 'POST'])
def index():
    return render_template('main.html')


@app.route('/prof', methods=['GET', 'POST'])
def prof():
    return render_template('main.html')


@app.route('/disc', methods=['GET', 'POST'])
def disc():
    return render_template('main.html')


@app.route('/topic', methods=['GET', 'POST'])
def topic():
    return render_template('main.html')


if __name__ == '__main__':
    host = 'localhost'
    while True:
        try:
            app.run(host=host, port=8000, debug=True)
        except Exception as e:
            print(e.__class__.__name__)
