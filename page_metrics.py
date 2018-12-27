import flask
import my_forms
import numpy

import func_find_path
from methods import func_metrics


metrics_page = flask.Blueprint(
    'metrics',
    __name__,
    template_folder='templates'
)


PATH = func_find_path.get_path()
GENERATED = False
HANDLED_PATH = False
HANDLED = False


@metrics_page.route('/metrics_test')
def test():
    return 'test_test_test'


@metrics_page.route('/metrics', methods=['GET', 'POST'])
def metrics_entered():
    global PATH, GENERATED, HANDLED_PATH, HANDLED
    form = my_forms.MetricsForm()

    # generated
    if (form.count_of_b_vector.data is not None) != (form.len_vectors.data is not None):
        flask.flash('Проверьте входные данные для генераци!')
    elif form.count_of_b_vector.data is not None and form.len_vectors.data is not None:
        path_to_gen = PATH + '/static/metrics/generated.txt'
        func_metrics.generator(
            len_vectors=form.len_vectors.data,
            lines_in_matrix=form.count_of_b_vector.data,
            path=path_to_gen
        )
        GENERATED = True
        return flask.redirect('/metric_view')

    # other path
    if form.path_to_data.data is not None:
        HANDLED_PATH = form.path_to_data.data
        return flask.redirect('/metric_view')

    # handle entered
    if form.handle_entered.data is not None:
        if form.handle_entered.data.strip() != '>' or form.handle_entered.data.strip() != '':
            file_name = PATH + '/static/metrics/handle_entered.txt'
            with open(file_name, 'w') as file:
                file.write(form.handle_entered.data)
            HANDLED = True
            return flask.redirect('/metric_view')

    return flask.render_template(
        'metrics.html',
        title='Метрики.',
        path_to_example='static/metrics/img/example_handle_entered.png',
        form=form
    )


@metrics_page.route('/metric_view')
def metrics_exit():
    global PATH, GENERATED, HANDLED_PATH, HANDLED
    if GENERATED:
        path_to_data = PATH + '/static/metrics/generated.txt'
        GENERATED = False
    elif not isinstance(HANDLED_PATH, bool) and not HANDLED_PATH == '':
        path_to_data = HANDLED_PATH
        HANDLED_PATH = False
    elif HANDLED:
        path_to_data = PATH + '/static/metrics/handle_entered.txt'
        HANDLED = False
    else:
        path_to_data = PATH + '/static/metrics/test.txt'
        flask.flash('Загружен пример.')
    p, vec_a, vec_b = func_metrics.read_data(path_to_data)

    answered = func_metrics.all_metrics(p, vec_a, vec_b)

    to_html_a = '( '
    for number in vec_a:
        to_html_a += str(number) + '; '
    to_html_a = to_html_a[:-2] + ' )'

    # check vector b (matrix or vector) in func_metrics line 159
    if isinstance(vec_b[0], numpy.ndarray):
        matrix_flag = True
        to_html_b = ''
        temp_b = list(vec_b)
        temp_b = [list(i) for i in temp_b]

    else:
        matrix_flag = False
        temp_b = [0]
        to_html_b = '( '
        for number in vec_b:
            to_html_b += str(number) + '; '
        to_html_b = to_html_b[:-2] + ' )'

    for key, value in answered.items():
        if numpy.isnan(value):
            answered[key] = 'Метрика не определена'

    # TODO: exit table for matrix

    return flask.render_template(
        'metrics_view.html',
        title='Расстояния.',
        p=p,
        vec_a=to_html_a,
        matrix_flag=matrix_flag,
        lines=len(temp_b),
        matrix=temp_b,
        vec_b=to_html_b,
        answ_dict=[(key, value) for key, value in answered.items()],
    )
