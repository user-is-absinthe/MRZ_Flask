from flask_wtf import FlaskForm
from wtforms import StringField, BooleanField, SubmitField
from wtforms.validators import DataRequired


class MatrixSize(FlaskForm):
    matrix_size = StringField('Введите размерность матрицы', validators=[DataRequired()])
    generate_matrix = BooleanField('Сгенерировать матрицу')
    do_this = SubmitField('OK!')
