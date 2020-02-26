from flask_wtf import FlaskForm
from wtforms import StringField, SubmitField
from wtforms.validators import Required, Length
from wtforms import StringField, SubmitField, PasswordField
from wtforms.validators import Required, Length, Email, EqualTo, ValidationError
from application.models import Users
from wtforms import StringField,SubmitField,PasswordField,BooleanField

class LoginForm(FlaskForm):
    email=StringField('Email',
        validators=[
            Required(),
            Email()
         ]
    )

    password=PasswordField('Password',
        validators=[
            Required()
        ]
    )

    remember=BooleanField('Remember Me')
    submit=SubmitField('Login')

class PostForm(FlaskForm):
    first_name = StringField('First Name',
        validators = [
            Required(),
            Length(min=2, max=30)
        ]
    )
    last_name = StringField('Last Name',
        validators = [
            Required(),
            Length(min=2, max=30)
        ]
    )
    title = StringField('Title',
        validators = [
            Required(),
            Length(min=2, max=100)
        ]
    )
    content = StringField('Content',
        validators = [
            Required(),
            Length(min=2, max=1000)
        ]
    )
    submit = SubmitField('Post!')


class RegistrationForm(FlaskForm):
    email = StringField('Email',
        validators = [
            Required(),
            Email()
        ]
    )
    password = PasswordField('Password',
        validators = [
            Required(),
        ]
    )
    confirm_password = PasswordField('Confirm Password',
        validators = [
            Required(),
            EqualTo('password')
        ]
    )
    submit = SubmitField('Sign Up')

    def validate_email(self, email):
        user = Users.query.filter_by(email=email.data).first()

        if user:
            raise ValidationError('Email already in use')
