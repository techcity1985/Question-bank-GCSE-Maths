from flask_wtf import FlaskForm
from wtforms import StringField, FileField, TextAreaField
from wtforms.validators import DataRequired

class QuestionForm(FlaskForm):
    question = TextAreaField('Question', validators=[DataRequired()])
    answer = TextAreaField('Answer', validators=[DataRequired()])
    image = FileField('Image File')
