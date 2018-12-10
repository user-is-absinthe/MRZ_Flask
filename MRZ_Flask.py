from flask import Flask
from flask import flash
from flask import render_template
from flask import redirect

from methods import nsko
from form_true_chromatic import MatrixSize
from methods import true_chromatic

app = Flask(__name__)
app.config['SECRET_KEY'] = 'you-will-never-guess'
app.debug = True


# @app.route('/')
# def hello_world():
#     return 'Hello World!'


@app.route('/')
@app.route('/algoritms')
def main_page():
    algoritms = {
        'true_chromatic': 'Раскраска графа.',
    }
    links = [
        '/true_chromatic'
    ]
    return render_template('algoritms.html', title='Заглавная страница.', algs=zip(links, algoritms.values()))


@app.route('/true_chromatic', methods=['GET', 'POST'])
def true_chromatic():
    form = MatrixSize()
    matrix_size_i = -98563
    try:
        # print(form.matrix_size.data)
        if form.matrix_size.data is not None:
            matrix_size_i = int(form.matrix_size.data)
    except ValueError:
        flash('Введено неверное значение количества вершин.')
    except TypeError:  # as tp:
        # flash(tp)
        flash('Введено неверное значение количества вершин.')
    if 0 < matrix_size_i < 65:
        # print(matrix_size_i)
        flash('Считаем, что в графе {} вершины.'.format(matrix_size_i))
        # print(form.generate_matrix.data)
        if form.generate_matrix.data:
            true_chromatic.generate_matrix(
                size=matrix_size_i,
                path='data/true_chromatic/temp_matrix.txt'
            )

    elif matrix_size_i != -98563:
        flash('Колчество вершин должно принадлежать диапазону (0, 65).')
    # if form.matrix_size.data():
    #     flash('Считаем, что в графе {} вершины.'.format(form.matrix_size.data))
    #     return redirect('/algoritms')
    # else:
    #     flash('Какая-то ошибка!')
    return render_template('true_chromatic.html', title='Раскраска графа.', form=form)


@app.route('/nsko')
def method_nsko():
    out = nsko.test_func('data\\nsko\input_file.txt')
    return str(out)


if __name__ == '__main__':
    # app.debug = True
    app.run()
