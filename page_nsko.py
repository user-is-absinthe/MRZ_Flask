import flask

from methods import func_nsko

import forms


nsko_page = flask.Blueprint(
    'nsko',
    __name__,
    template_folder='templates'
)


@nsko_page.route('/nsko_test')
def test_f():
    test_path = '/Users/owl/Pycharm/PycharmProjects/MRZ_Flask/static/nsko/input_file.txt'
    test_answ = func_nsko.nsko(test_path)
    return str(test_answ)


@nsko_page.route('/nsko')
def nsko_entered():
    form = forms.NskoForm()
    pass
