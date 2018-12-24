from flask_wtf import FlaskForm
from wtforms.validators import DataRequired
import wtforms


class TrueChromaticForm(FlaskForm):
    matrix_size = wtforms.StringField('Введите размерность матрицы', validators=[DataRequired()])
    generate_matrix = wtforms.BooleanField('Сгенерировать матрицу')
    handle_matrix = wtforms.BooleanField('Ввести вручную?')
    handle_matrix_entered = wtforms.StringField('Ведите матрицу смежности.')
    path_to_another_matrix = wtforms.StringField('Введите абсолютный путь до файла с матрицей.')
    do_this = wtforms.SubmitField('Получить ответ.')


class NskoForm(FlaskForm):
    count_of_classes = wtforms.IntegerField('Введите количество классов.')
    count_of_vectors = wtforms.IntegerField('Введите количество векторов в классе.')
    handle_entered = wtforms.StringField('Введите данные вручную.')
    path_to_data = wtforms.StringField('Введите путь до файла с данными.')
    do_this = wtforms.SubmitField('Получить ответ.')
