from flask_wtf import FlaskForm
from wtforms import StringField, SubmitField, PasswordField, BooleanField
from wtforms.validators import DataRequired, Length, EqualTo, ValidationError
from application.models import Users
from flask_login import current_user

class RegistrationForm(FlaskForm):
    username = StringField('Username',
        validators = [
            DataRequired(),
            Length(min=2, max=30)
        ]
    )
    first_name = StringField('First Name',
        validators = [
            DataRequired(),
            Length(min=2, max=30)
        ]
    )
    last_name = StringField('Last Name',
        validators = [
            DataRequired(),
            Length(min=3, max=30)
        ]
    )
    password = PasswordField('Password',
        validators = [
            DataRequired(),
        ]
    )
    confirm_password = PasswordField('Confirm Password',
        validators = [
            DataRequired(),
            EqualTo('password')
        ]
    )
    submit = SubmitField('Sign Up')

    def validate_email(self, username):
        user = Users.query.filter_by(username=username.data).first()

        if user:
            raise ValidationError('Username already in use')

class LoginForm(FlaskForm):
    username = StringField('Username',
        validators=[
            DataRequired(),
            Length(min=2, max=30)
        ]
    )

    password = PasswordField('Password',
        validators=[
            DataRequired()
        ]
    )

    remember = BooleanField('Remember Me')
    submit = SubmitField('Login')

class QuestionForm(FlaskForm):
    ask = StringField('Question',
        validators = [
            DataRequired(),
            Length(min=4, max=100)
        ]
    )
    submit = SubmitField('Ask Question')

class AnswerForm(FlaskForm):
    ans = StringField('Answer',
        validators = [
            DataRequired(),
            Length(min=4, max=100)
        ]
    )
    submit = SubmitField('Answer Question')

