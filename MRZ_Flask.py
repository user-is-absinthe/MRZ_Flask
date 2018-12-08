from flask import Flask
# import page_nsko
from methods import nsko

app = Flask(__name__)


@app.route('/')
def hello_world():
    return 'Hello World!'


@app.route('/nsko')
def method_nsko():
    out = nsko.


if __name__ == '__main__':
    app.debug = True
    app.run()
