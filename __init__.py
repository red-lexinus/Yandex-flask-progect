from config import app  # , login_manager
from flask import render_template, request
from models import *
from forms import *
import requests


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


@app.route('/test', methods=['GET', 'POST'])
def test():
    return render_template('8values/index.html')


@app.route('/test/instructions', methods=['GET', 'POST'])
def instructions():
    return render_template('8values/instructions.html')


@app.route('/test/quiz', methods=['GET', 'POST'])
def quiz():
    return render_template('8values/quiz.html')


@app.route('/test/results', methods=['GET', 'POST'])
def res():
    e = request.args.get('e', default=1, type=float)
    d = request.args.get('d', default=1, type=float)
    g = request.args.get('g', default=1, type=float)
    s = request.args.get('s', default=1, type=float)
    return render_template('8values/results.html')


if __name__ == '__main__':
    host = 'localhost'
    while True:
        try:
            app.run(host=host, port=8000, debug=True)
        except Exception as e:
            print(e.__class__.__name__)
