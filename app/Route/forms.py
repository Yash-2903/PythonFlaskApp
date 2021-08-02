"""Form object declaration."""
from flask_wtf import FlaskForm
from wtforms import StringField, TextAreaField, TextField, SubmitField, PasswordField, DateField, SelectField
from wtforms.validators import DataRequired, EqualTo, Length, Email, URL


class ContactForm(FlaskForm):
    """Contact form."""
    name = StringField(
        'Name',
        [DataRequired()]
    )
    email = StringField(
        'Email',
        [
            Email(message="Not a valid email address."),
            DataRequired()
        ]
    )
    body = TextField(
        'Message',
        [
            DataRequired(),
            Length(min=4, message='Your message is too short.')
        ]
    )
    # recaptcha = RecaptchaField()
    submit = SubmitField('Submit')


class SigninForm(FlaskForm):
    """Sign in for a user account."""
    email = StringField(
        "Email",
        [
            Email(message='Not a valid email address.'),
            DataRequired()
        ]
    )
    password = PasswordField(
        "Password",
        [
            DataRequired(message="Please enter a password."),
            Length(min=6, message='Select a stronger password.')
        ]
    )
    submit = SubmitField("Submit")