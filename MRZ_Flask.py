import os

from flask import Flask
from flask import render_template

from methods import func_nsko
import func_find_path

import page_true_chromatic


app = Flask(__name__)
app.config['SECRET_KEY'] = 'you-will-never-guess'
app.debug = True
app.register_blueprint(page_true_chromatic.true_chromatic_page)


temp_path = func_find_path.get_path()
if not os.path.exists(temp_path + '/static/true_chromatic/img'):
    os.mkdir(temp_path + '/static/true_chromatic/img')


@app.route('/')
@app.route('/algoritms')
def main_page():
    alg = {
        'Раскраска графа.': '/true_chromatic',
    }
    return render_template(
        'algoritms.html',
        title='Заглавная страница.',
        algs=[(value, key) for key, value in alg.items()]
    )


@app.route('/nsko')
def method_nsko():
    out = func_nsko.test_func('data\\nsko\input_file.txt')
    return str(out)


if __name__ == '__main__':
    app.run()
