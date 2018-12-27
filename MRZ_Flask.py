from flask import Flask
from flask import render_template


import page_true_chromatic
import page_nsko
import page_metrics


app = Flask(__name__)
app.config['SECRET_KEY'] = 'you-will-never-guess'
app.debug = True

app.register_blueprint(page_true_chromatic.true_chromatic_page)
app.register_blueprint(page_nsko.nsko_page)
app.register_blueprint(page_metrics.metrics_page)


@app.route('/')
@app.route('/algoritms')
def main_page():
    alg = {
        'Раскраска графа.': '/true_chromatic',
        # 'ТЕСТ_НСКО.': '/nsko_test',
        'НСКО.': '/nsko',
        # 'ТЕСТ_метрики.': '/metrics_test',
        'Метрики.': '/metrics',
    }

    return render_template(
        'algoritms.html',
        title='Заглавная страница.',
        algs=[(value, key) for key, value in alg.items()]
    )


if __name__ == '__main__':
    app.run()
