import os

from flask import Flask
from flask import render_template

from methods import func_nsko
import func_find_path

import page_true_chromatic
import page_nsko


app = Flask(__name__)
app.config['SECRET_KEY'] = 'you-will-never-guess'
app.debug = True

app.register_blueprint(page_true_chromatic.true_chromatic_page)
app.register_blueprint(page_nsko.nsko_page)


@app.route('/')
@app.route('/algoritms')
def main_page():
    alg = {
        'Раскраска графа.': '/true_chromatic',
        'ТЕСТ_НСКО.': '/nsko_test',
        'НСКО.': '/nsko',
    }
    return render_template(
        'algoritms.html',
        title='Заглавная страница.',
        algs=[(value, key) for key, value in alg.items()]
    )


if __name__ == '__main__':
    app.run()
