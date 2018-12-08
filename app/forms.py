from flask_wtf import FlaskForm
from wtforms import StringField, TextAreaField, SubmitField, PasswordField, BooleanField, TimeField, SelectMultipleField, SelectField
from wtforms.validators import DataRequired, EqualTo, Email, ValidationError
from wtforms.fields.html5 import DateField
from app import db
from app.models import Artist, Performance, ArtistToPerformance, Location, Genre, ArtistToGenre


class LoginForm(FlaskForm):
    email = StringField('Email', validators=[DataRequired()])
    password = PasswordField('Password', validators=[DataRequired()])
    remember_me = BooleanField('Remember Me')
    submit = SubmitField('Sign In')


class RecommendationForm(FlaskForm):
    genres = SelectMultipleField("Genres", coerce=int, choices=[])
    submit = SubmitField('Submit')


class RegistrationForm(FlaskForm):
    email = StringField('Email', validators=[DataRequired(), Email()])
    password = PasswordField('Password', validators=[DataRequired()])
    password2 = PasswordField('Re-enter Password', validators=[DataRequired(), EqualTo('password')])
    artistName = StringField('Name', validators=[DataRequired()])
    bio = StringField('Biography')
    #add genre back in
    submit = SubmitField('Register')


    def validate_email(self, email):
        user = Artist.query.filter_by(email=email.data).first()
        if user is not None:
            raise ValidationError('Use another email. This one is already taken.')


class EventSignUp (FlaskForm):
    date = DateField('Date', format='%Y-%m-%d', validators=DataRequired)
    time = TimeField('Time', validators=DataRequired)
    location = StringField('Location', validators=DataRequired)
    submit = SubmitField('Add New Event')


class EditProfile (FlaskForm):
    username = StringField('Change Username')
    email = StringField('Change Email')
    artistName = StringField('Change artist name')
    bio = StringField('Change Biography')
    genre = StringField('Change Genres')  #could use autofill
    submit = SubmitField('Save')

#needs review
class RecommendationForm (FlaskForm):
    genres = SelectMultipleField('Select Genres')