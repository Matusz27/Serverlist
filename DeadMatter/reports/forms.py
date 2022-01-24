from flask_wtf import FlaskForm
from flask_wtf.file import FileField, FileAllowed
from wtforms.validators import DataRequired, Length, Optional
from wtforms import SubmitField, TextAreaField, SelectField, StringField








class report_server_form(FlaskForm):
    
    problem = SelectField('Problem', choices=[
                          ('Spam', 'Spam'), ('Obscene', 'Vulgar/Obscene content'),
                          ('Problem', "Link or IP doesn't work"), ('Safety Problem', "Illegal or Safty Issue")])

    email = StringField('Email*', validators=[DataRequired()])

    description = TextAreaField('Description*', validators=[DataRequired(), Length(
        min=10, max=1000)])

    submit = SubmitField("Submit Now")


class report_page_form(FlaskForm):

    problem = SelectField('Problem*', choices=[
        ('Feature', 'Feature'), ('Typo', 'Typo or misspelling'),
        ('Problem', "Page doesn't work"), ('Safety', "Safety Issue")
    ])
    
    email = StringField('Email*', validators=[DataRequired()])

    description = TextAreaField('Description*', validators=[DataRequired(), Length(
        min=10, max=1000)])

    submit = SubmitField("Submit Now")
