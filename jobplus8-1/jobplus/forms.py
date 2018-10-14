from flask_wtf import FlaskForm
from wtforms import StringField, PasswordField, SubmitField,BooleanField
from wtforms.validators import Length,Email,EqualTo,DataRequired

class RegisterForm(FlaskForm):
    username = StringField('user name',validators=[DataRequired(),Length(3,24)])
    email = StringField('email',validators=[DataRequired(),Email()])
    password = PasswordField('password',validators=[DataRequired(),Length(6,24)])
    repeat_password = PasswordField('repeat password',validators=[DataRequired(),EqualTo('password')])
    submit = SubmitField('submit')

class LoginForm(FlaskForm):
    email = StringField('email',validators=[DataRequired(),Email()])
    password = PasswordField('password',validators=[DataRequired(),Length(6,24)])
    remeber_me = BooleanField('remeber me')
    submit = SubmitField('submit')


