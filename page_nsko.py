import flask
import forms
import time

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
    form = forms.NskoForm()

    # generated
    if (form.len_vectors.data is not None) != (form.count_of_vectors.data is not None):
        flask.flash('Проверьте входные данные для генераци!')
    elif form.len_vectors.data is not None and form.count_of_vectors.data is not None:
        func_nsko.generator(form.len_vectors.data, form.count_of_vectors.data, PATH + '/static/nsko/generated.txt')
        GENERATED = True
        return flask.redirect('/nsko_view')

    # other path
    print(form.path_to_data.data)
    if form.path_to_data.data is not None:
        HANDLED_PATH = True
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
        HANDLED_PATH = False

    array_of_x, array_of_classes = func_load_from_file.load_for_nsko(path_to_data)

    answered = func_nsko.additional_constructions(ar_x=array_of_x, ar_cl=array_of_classes)

    answered_to_html = str(answered)
    answered_to_html = answered_to_html.replace('[[', '[')
    answered_to_html = answered_to_html.replace(']]', ']')

    path_to_img = None
    if len(array_of_x[0]) == 3:

        path_to_img = PATH + '/static/nsko/img/temp/nsko_{}'.format(str(time.time()).replace('.', '')) + '.png'
        func_nsko.plot_nsko()
        pass

    return flask.render_template(
        'nsko_view.html',
        title='Результат НСКО.',
        answered=answered_to_html,
        column=1,
        lines=1,
        matrix=[[1]]
    )
