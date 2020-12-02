from flask_wtf import FlaskForm
from wtforms import StringField, PasswordField, SubmitField
from wtforms.validators import DataRequired, Length, Email


class LoginForm(FlaskForm):
    username = StringField('Username', validators=[
        DataRequired()])
    password = PasswordField('Password', validators=[
        DataRequired(),
        Length(min=8, message="Length must be at least 8 characters")])
    submit = SubmitField('Submit')


class SignUpForm(FlaskForm):
    f_name = StringField('First Name', validators=[
        DataRequired()])
    l_name = StringField('Last Name', validators=[
        DataRequired()])
    username = StringField('Username', validators=[
        DataRequired()])
    email = StringField('Email', validators=[
        DataRequired(),
        Email(message="Must enter a valid email address")])
    password = PasswordField('Password', validators=[
        DataRequired(),
        Length(min=8, message="Length must be at least 8 characters")])
    submit = SubmitField('Submit')
