import os
import time

from flask import flash
from flask import render_template
from flask import redirect
from flask import Blueprint

import forms
from methods import func_true_chromatic
from methods import func_read_from_csv as csv
import func_find_path


true_chromatic_page = Blueprint(
    'true_chromatic',
    __name__,
    template_folder='templates'
)


CHROMATIC_PATH_TO_MATRIX = ''
CHROMATIC_HANDLE_MATRIX = False


temp_path = func_find_path.get_path()
if not os.path.exists(temp_path + '/static/true_chromatic/img'):
    os.mkdir(temp_path + '/static/true_chromatic/img')


@true_chromatic_page.route('/true_chromatic', methods=['GET', 'POST'])
def true_chromatic():
    global CHROMATIC_PATH_TO_MATRIX, CHROMATIC_HANDLE_MATRIX
    form = forms.TrueChromaticForm()
    matrix_size_i = -98563
    # ввод из файла
    if form.path_to_another_matrix.data is not None and not form.path_to_another_matrix.data == '':
        # print(form.path_to_another_matrix.data)
        CHROMATIC_PATH_TO_MATRIX = form.path_to_another_matrix.data
        to_check = csv.open_alien_matrix(CHROMATIC_PATH_TO_MATRIX)
        # print('awdaw', CHROMATIC_PATH_TO_MATRIX)
        if to_check != 'bad':
            return redirect('/true_chromatic_view')
        else:
            flash('Проверте файл с данными и/или путь к нему.')

    # автогенерация
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
            path = func_find_path.get_path()
            func_true_chromatic.generate_matrix_in(
                size=matrix_size_i,
                # path='data/true_chromatic/temp_matrix.txt'
                path=path + '/static/true_chromatic/temp_matrix.txt'
            )
            return redirect('/true_chromatic_view')

    elif matrix_size_i != -98563:
        flash('Колчество вершин должно принадлежать диапазону (0, 65).')

    # ввод ручками
    # print(form.handle_matrix_entered.data)
    # if form.handle_matrix.data:
    if form.handle_matrix_entered.data is not None and not form.handle_matrix_entered.data == '':
        to_write = form.handle_matrix_entered.data
        path = func_find_path.get_path()
        save_matrix = path + '/static/true_chromatic/temp_matrix_hand.txt'
        with open(save_matrix, 'w') as file:
            file.write(to_write)

        to_check = csv.open_alien_matrix(save_matrix)
        if to_check != 'bad':
            CHROMATIC_HANDLE_MATRIX = True
            return redirect('/true_chromatic_view')
        else:
            flash('Проверте вводимые данные.')

    return render_template(
        'true_chromatic.html',
        title='Раскраска графа.',
        path_to_examle='static/true_chromatic/example_handle_entered.png',
        form=form
    )


@true_chromatic_page.route('/true_chromatic_view')
def true_chromatic_view():
    global CHROMATIC_PATH_TO_MATRIX, CHROMATIC_HANDLE_MATRIX
    # graph = None
    # print('wa,,,', CHROMATIC_PATH_TO_MATRIX)
    path = func_find_path.get_path() + '/static/true_chromatic/'
    # if CHROMATIC_PATH_TO_MATRIX != '':
    #     path_to_matrix = CHROMATIC_PATH_TO_MATRIX
    #     CHROMATIC_PATH_TO_MATRIX = ''
    # else:
    #     path_to_matrix = path + 'temp_matrix.txt'

    if CHROMATIC_HANDLE_MATRIX:
        path_to_matrix = path + 'temp_matrix_hand.txt'
        CHROMATIC_HANDLE_MATRIX = False
    elif CHROMATIC_PATH_TO_MATRIX != '':
        path_to_matrix = CHROMATIC_PATH_TO_MATRIX
        CHROMATIC_PATH_TO_MATRIX = ''
    else:
        path_to_matrix = path + 'temp_matrix.txt'

    # remove files
    path_to_img = path + 'img/'
    files_to_remove = os.listdir(path_to_img)
    for filename in files_to_remove:
        os.remove(path_to_img + filename)

    matrix_str = csv.open_matrix(path_to_matrix)
    graph = func_true_chromatic.create_graph(matrix_str)
    temp_name = time.time()
    path_to_mono_graph = path_to_img + 'monochromgraph_{}.png'.format(str(temp_name).replace('.', ''))
    # os.remove(path_to_mono_graph)
    func_true_chromatic.draw_graph(graph=graph, path_to_save=path_to_mono_graph)
    chromatic_number, colors = func_true_chromatic.find_colors(graph)
    path_to_many_graph = path_to_img + 'chromgraph_{}.png'.format(str(temp_name).replace('.', ''))
    # os.remove(path_to_many_graph)
    func_true_chromatic.draw_graph(graph=graph, colors=colors, path_to_save=path_to_many_graph)
    return render_template(
        'true_chromatic_view.html',
        file=matrix_str,
        stb=len(matrix_str[0]),
        str=len(matrix_str),
        # path_to_mono_graph=func_find_path.fix_path(path_to_mono_graph),
        path_to_mono_graph='static/true_chromatic/img/monochromgraph_{}.png'.format(str(temp_name).replace('.', '')),
        chromatic_number=chromatic_number,
        path_to_many_graph='static/true_chromatic/img/chromgraph_{}.png'.format(str(temp_name).replace('.', ''))
    )
