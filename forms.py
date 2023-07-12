from flask_wtf import FlaskForm
from wtforms import FileField, SubmitField
from wtforms.validators import InputRequired

class File(FlaskForm):
    file = FileField("File", validators=[InputRequired()])
    submit = SubmitField("Proceed")

class Column(FlaskForm):
    submit = SubmitField()