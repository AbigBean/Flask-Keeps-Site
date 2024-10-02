from flask_wtf import FlaskForm
from wtforms.validators import InputRequired, Email, DataRequired
from wtforms import StringField, TextAreaField, SubmitField, PasswordField



class LoginForm(FlaskForm):
	username = StringField ('Username', validators=[DataRequired()])
	password = PasswordField('Password', validators=[DataRequired()])
	submit = SubmitField('Sunmit')

class RegisterForm(FlaskForm):
	name = StringField('Name')
	username = StringField('Username', validators=[DataRequired()])
	password = PasswordField('Password', validators=[DataRequired()])
	email = StringField('Email', validators=[DataRequired(), Email()])
	submit = SubmitField('Submit')

class NoteForm(FlaskForm):
    note = TextAreaField('Write your note here', validators=[DataRequired()])


class ResetPasswordRequestForm(FlaskForm):
	email = StringField('Email', validators=[DataRequired(), Email()])
	submit = SubmitField('Sent request')

class ResetPasswordForm(FlaskForm):
	password = PasswordField('New Password', validators=[DataRequired()])
	submit = SubmitField('Reset Password')
