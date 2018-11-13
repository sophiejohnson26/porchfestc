from datetime import datetime
from app import app, db, login
from flask_login import UserMixin
from werkzeug.security import generate_password_hash, check_password_hash
import jwt


class Artist(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    artistName = db.Column(db.String(64), index=True, unique=True)
    bio = db.Column(db.String(600))
    genreId = db.Column(db.Integer)
    artistPerformances= db.relationship('ArtistToPerformance')
    artistGenre = db.relationship('ArtistToGenre')
    username = db.Column(db.String(64), index=True, unique=True)
    email = db.Column(db.String(120), index=True, unique=True)
    password_hash = db.Column(db.String(128))

    def __repr__(self):
        return '<User {}>'.format(self.username)

    def set_password(self, password):
        self.password_hash = generate_password_hash(password)

    def check_password(self, password):
        return check_password_hash(self.password_hash, password)

    def get_reset_password_token(self, expires_in=600):
        return jwt.encode(
            {'reset_password': self.id, 'exp': time() + expires_in},
            app.config['SECRET_KEY'], algorithm='HS256').decode('utf-8')

    @staticmethod
    def verify_reset_password_token(token):
        try:
            id = jwt.decode(token, app.config['SECRET_KEY'],
                            algorithms=['HS256'])['reset_password']
        except:
            return
        return Artist.query.get(id)


@login.user_loader
def load_user(id):
    return Artist.query.get(int(id))


class Performance(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    time = db.Column(db.DateTime, index=True, default=datetime.utcnow)
    date = db.Column(db.DateTime, index=True, default=datetime.utcnow)
    locationId = db.Column(db.Integer, db.ForeignKey('location.id'))
    artistPerformances = db.relationship('ArtistToPerformance')


class Location(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(64), index=True, unique=True)
    location = db.Column(db.String(64))


class ArtistToPerformance(db.Model):
    artistID = db.Column(db.Integer, db.ForeignKey('artist.id'),  primary_key=True)
    performanceID = db.Column(db.Integer, db.ForeignKey('performance.id'), primary_key=True)
    artist = db.relationship('Artist')
    performance = db.relationship('Performance')


class Genre(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    genre = db.Column(db.String(120))
    artistGenre=db.relationship('ArtistToGenre')


class artistToGenre(db.Model):
    artistID = db.Column(db.Integer, db.ForeignKey('artist.id'), primary_key=True)
    genreID = db.Column(db.Integer, db.ForeignKey('genre.id'), primary_key=True)
    artist = db.relationship('Artist')
    genre = db.relationship('Genre')








