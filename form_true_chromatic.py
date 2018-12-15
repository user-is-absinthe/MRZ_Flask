from flask_wtf import FlaskForm
from wtforms import StringField, BooleanField, SubmitField
from wtforms.validators import DataRequired


class MatrixSize(FlaskForm):
    matrix_size = StringField('Введите размерность матрицы', validators=[DataRequired()])
    generate_matrix = BooleanField('Сгенерировать матрицу')
    handle_matrix = BooleanField('Ввести вручную?')
    handle_matrix_entered = StringField('Ведите матрицу смежности.')
    path_to_another_matrix = StringField('Введите абсолютный путь до файла с матрицей.')
    do_this = SubmitField('OK!')
