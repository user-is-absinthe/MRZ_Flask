# import os
from flask import Flask
from flask import flash
from flask import render_template
from flask import redirect

from methods import func_nsko
from form_true_chromatic import MatrixSize
from methods import func_true_chromatic
from methods import func_read_from_csv as csv
# from methods import func_find_path

app = Flask(__name__)
app.config['SECRET_KEY'] = 'you-will-never-guess'
app.debug = True

CHROMATIC_PATH_TO_MATRIX = ''
CHROMATIC_HANDLE_MATRIX = False


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
    global CHROMATIC_PATH_TO_MATRIX, CHROMATIC_HANDLE_MATRIX
    form = MatrixSize()
    matrix_size_i = -98563
    # ввод из файла
    if form.path_to_another_matrix.data is not None and not form.path_to_another_matrix.data == '':
        CHROMATIC_PATH_TO_MATRIX = form.path_to_another_matrix.data
        to_check = csv.open_alien_matrix(CHROMATIC_PATH_TO_MATRIX)
        if to_check != 'bad':
            return redirect('/true_chromatic_view')
        else:
            flash('Проверте файл с данными и/или путь к нему.')

    if form.matrix_size.data is not None and not form.matrix_size.data == '':
        try:
            # print(form.matrix_size.data)
            matrix_size_i = int(form.matrix_size.data)
        except ValueError:
            flash('Введено неверное значение количества вершин.')
        except TypeError:  # as tp:
            # flash(tp)
            flash('Введено неверное значение количества вершин.')
        if 0 < matrix_size_i < 65:
            # print(matrix_size_i)
            flash('Количество вершин графа: {}.'.format(matrix_size_i))
            # print(form.generate_matrix.data)

            # авто генерация
            if form.generate_matrix.data:
                path = func_true_chromatic.get_path()
                func_true_chromatic.generate_matrix_in(
                    size=matrix_size_i,
                    # path='data/true_chromatic/temp_matrix.txt'
                    path=path + '/../static/true_chromatic/temp_matrix.txt'
                )
                return redirect('/true_chromatic_view')

    elif matrix_size_i != -98563:
        flash('Колчество вершин должно принадлежать диапазону (0, 65).')

    # ввод ручками
    # print(form.handle_matrix_entered.data)
    if form.handle_matrix.data:
        to_write = form.handle_matrix_entered.data
        path = func_true_chromatic.get_path()
        save_matrix = path + '/../static/true_chromatic/temp_matrix_hand.txt'
        with open(save_matrix, 'w') as file:
            file.write(to_write)

        to_check = csv.open_alien_matrix(save_matrix)
        if to_check != 'bad':
            CHROMATIC_HANDLE_MATRIX = True
            return redirect('/true_chromatic_view')
        else:
            flash('Проверте вводимые данные.')

    return render_template('true_chromatic.html', title='Раскраска графа.', form=form)


@app.route('/true_chromatic_view')
def true_chromatic_view():
    global CHROMATIC_PATH_TO_MATRIX, CHROMATIC_HANDLE_MATRIX
    # graph = None
    path = func_true_chromatic.get_path() + '/../static/true_chromatic/'
    if CHROMATIC_PATH_TO_MATRIX != '':
        path_to_matrix = CHROMATIC_PATH_TO_MATRIX
        CHROMATIC_PATH_TO_MATRIX = ''
    else:
        path_to_matrix = path + 'temp_matrix.txt'

    if CHROMATIC_HANDLE_MATRIX:
        path_to_matrix = path + 'temp_matrix_hand.txt'
        CHROMATIC_HANDLE_MATRIX = False
    else:
        path_to_matrix = path + 'temp_matrix.txt'

    matrix_str = csv.open_matrix(path_to_matrix)
    graph = func_true_chromatic.create_graph(matrix_str)
    path_to_mono_graph = path + 'monochromgraph.png'
    # os.remove(path_to_mono_graph)
    func_true_chromatic.draw_graph(graph=graph, path_to_save=path_to_mono_graph)
    chromatic_number, colors = func_true_chromatic.find_colors(graph)
    path_to_many_graph = path + 'chromgraph.png'
    # os.remove(path_to_many_graph)
    func_true_chromatic.draw_graph(graph=graph, colors=colors, path_to_save=path_to_many_graph)
    return render_template(
        'true_chromatic_view.html',
        file=matrix_str,
        # path_to_mono_graph=func_find_path.fix_path(path_to_mono_graph),
        path_to_mono_graph='static/true_chromatic/monochromgraph.png',
        chromatic_number=chromatic_number,
        path_to_many_graph='static/true_chromatic/chromgraph.png'
    )


@app.route('/nsko')
def method_nsko():
    out = func_nsko.test_func('data\\nsko\input_file.txt')
    return str(out)


if __name__ == '__main__':
    # app.debug = True
    app.run()
