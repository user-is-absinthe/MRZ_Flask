import flask
import my_forms
import time
import os

from methods import func_nsko
from methods import func_load_from_file
import func_find_path


nsko_page = flask.Blueprint(
    'nsko',
    __name__,
    template_folder='templates'
)


GENERATED = False
HANDLED = False
HANDLED_PATH = ''
PATH = func_find_path.get_path()


@nsko_page.route('/nsko_test')
def test_f():
    test_path = '/Users/owl/Pycharm/PycharmProjects/MRZ_Flask/static/nsko/input_file.txt'
    test_answ = func_nsko.nsko(test_path)
    return str(test_answ)


@nsko_page.route('/nsko', methods=['GET', 'POST'])
def nsko_entered():
    global GENERATED, HANDLED, HANDLED_PATH, PATH
    form = my_forms.NskoForm()

    # generated
    if (form.len_vectors.data is not None) != (form.count_of_vectors.data is not None):
        flask.flash('Проверьте входные данные для генераци!')
    elif form.len_vectors.data is not None and form.count_of_vectors.data is not None:
        func_nsko.generator(form.len_vectors.data, form.count_of_vectors.data, PATH + '/static/nsko/generated.txt')
        GENERATED = True
        return flask.redirect('/nsko_view')

    # other path
    # print(form.path_to_data.data)
    if form.path_to_data.data is not None:
        HANDLED_PATH = form.path_to_data.data
        return flask.redirect('/nsko_view')

    # handle entered
    if form.handle_entered.data is not None:
        if form.handle_entered.data.strip() != '>' or form.handle_entered.data.strip() != '':
            func_nsko.save_data(PATH + '/static/nsko/handle_entered.txt', form.handle_entered.data.strip())
            HANDLED = True
            return flask.redirect('/nsko_view')

    return flask.render_template(
        'nsko.html',
        title='Алгоритм НСКО.',
        path_to_example='static/nsko/img/example_handle_entered.png',
        form=form,
    )


@nsko_page.route('/nsko_view')
def nsko_result():
    global GENERATED, HANDLED, HANDLED_PATH, PATH

    path_to_data = PATH + '/static/nsko/input_file.txt'

    if GENERATED:
        path_to_data = PATH + '/static/nsko/generated.txt'
        GENERATED = False
    elif HANDLED:
        path_to_data = PATH + '/static/nsko/handle_entered.txt'
        HANDLED = False
    elif not isinstance(HANDLED_PATH, bool):
        path_to_data = HANDLED_PATH
        if str(path_to_data) == '':
            flask.flash('Загружен пример.')
            path_to_data = PATH + '/static/nsko/input_file.txt'
        HANDLED_PATH = False

    array_of_x, array_of_classes = func_load_from_file.load_for_nsko(path_to_data)
    # print(array_of_x, array_of_classes)

    answered = func_nsko.additional_constructions(ar_x=array_of_x, ar_cl=array_of_classes)
    # print(answered)

    answered_to_html = str(answered)
    answered_to_html = answered_to_html.replace('[[', '[')
    answered_to_html = answered_to_html.replace(']]', ']')

    path_to_img = None
    if len(array_of_x[0]) == 3:
        path_to_img_dir = PATH + '/static/nsko/img/temp/'

        files_to_remove = os.listdir(path_to_img_dir)
        for filename in files_to_remove:
            os.remove(path_to_img_dir + filename)

        temp_name = str(time.time()).replace('.', '')
        path_to_img_save = path_to_img_dir + '/nsko_{}'.format(temp_name) + '.png'
        func_nsko.plot_nsko(path_to_img_save, array_of_x, answered)
        path_to_img = 'static/nsko/img/temp/nsko_' + temp_name + '.png'
        'static/nsko/img/temp/nsko_15457466688663812.png'

    first_class = list()
    second_class = list()
    for vector in array_of_x:
        if vector[-1] == 1:
            first_class.append(vector[:-1])
        else:
            second_class.append([-1 * i for i in vector[:-1]])

    return flask.render_template(
        'nsko_view.html',
        title='Результат НСКО.',
        answered=answered_to_html,
        lines_1=len(first_class),
        lines_2=len(second_class),
        first_class=first_class,
        second_class=second_class,
        path_to_img=path_to_img
    )
