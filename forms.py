from flask_wtf import FlaskForm
from wtforms import StringField, TextAreaField, FileField, SelectField, PasswordField, SubmitField
from wtforms.validators import DataRequired, Length, Email, EqualTo
from flask_wtf.file import FileAllowed
from models import Category

class QuestionForm(FlaskForm):
    question = TextAreaField('Question', validators=[DataRequired(), Length(min=10)])
    answer = TextAreaField('Answer', validators=[DataRequired(), Length(min=1)])
    image_file = FileField('Image File', validators=[FileAllowed(['jpg', 'png', 'jpeg'], 'Images only!')])
    category = SelectField('Category', coerce=int)
    submit = SubmitField('Submit')

    def __init__(self, *args, **kwargs):
        super(QuestionForm, self).__init__(*args, **kwargs)
        self.category.choices = [(category.id, category.name) for category in Category.query.all()]
