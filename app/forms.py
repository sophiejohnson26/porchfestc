from flask_wtf import *
from wtforms import *
from wtforms.validators import *
from wtforms.fields.html5 import *
from app import db
from app.models import *


class LoginForm(FlaskForm):
    email = StringField('Email', validators=[DataRequired()])
    password = PasswordField('Password', validators=[DataRequired()])
    remember_me = BooleanField('Remember Me')
    submit = SubmitField('Sign In')


class RecommendationForm(FlaskForm):
    genre = SelectField('Genres', choices=[("folk", "Folk"),('rock', "Rock"), ("hip_hop", "Hip Hop"),("pop", "Pop"), ("RB", "R&B"), ("indie", "Indie")])
    submit = SubmitField('Submit')


class RegistrationForm(FlaskForm):
    artistName = StringField('Name', validators=[DataRequired()])
    bio = StringField('Biography')
    genre = SelectField('Genres', choices=[("folk", "Folk"),('rock', "Rock"), ("hip_hop", "Hip Hop"),("pop", "Pop"), ("RB", "R&B"), ("indie", "Indie")])
    email = StringField('Email', validators=[DataRequired(), Email()])
    password = PasswordField('Password', validators=[DataRequired()])
    password2 = PasswordField('Re-enter Password', validators=[DataRequired(), EqualTo('password')])
    submit = SubmitField('Register')

    def validate_email(self, email):
        user = Artist.query.filter_by(email=email.data).first()
        if user is not None:
            raise ValidationError('Use another email. This one is already taken.')


class EventSignUp (FlaskForm):
    date = DateTimeField('Date',validators=[validators.InputRequired()], format="%d%b%Y",
                          default=datetime.utcnow)
    time = DateTimeField( 'Time',validators=[validators.InputRequired()], format="%H:%M",
                         default=datetime.utcnow)
    location = StringField('Location', validators=[DataRequired()])
    submit = SubmitField('Add New Event')


class EditProfile (FlaskForm):
    email = StringField('Change Email')
    artistName = StringField('Change artist name')
    bio = StringField('Change Biography')
    genre = SelectField('Genres', choices=[("folk", "Folk"),('rock', "Rock"), ("hip_hop", "Hip Hop"),("pop", "Pop"), ("RB", "R&B"), ("indie", "Indie")])
    submit = SubmitField('Save')

class EditPerfomance(FlaskForm):
    date = DateTimeField('Date', validators=[validators.InputRequired()], format="%d%b%Y",
                         default=datetime.utcnow)
    time = DateTimeField('Time', validators=[validators.InputRequired()], format="%H:%M",
                         default=datetime.utcnow)
    location = StringField('Location', validators=[DataRequired()])
    submit = SubmitField('Save')
    delete = SubmitField('Delete')

class ResetPasswordRequestForm(FlaskForm):
    email = StringField('Email', validators=[DataRequired(), Email()])
    submit = SubmitField('Request Password Reset')

class ResetPasswordForm(FlaskForm):
    password = PasswordField('Password', validators=[DataRequired()])
    password2 = PasswordField(
        'Repeat Password', validators=[DataRequired(), EqualTo('password')])
    submit = SubmitField('Request Password Reset')

