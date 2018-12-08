from datetime import datetime
from flask import render_template, flash, redirect, url_for, request
from flask_login import login_user, logout_user, current_user, login_required
from werkzeug.urls import url_parse
from app import app, db
from app.forms import *
from app.models import *

@app.route('/')
@app.route('/index')
def index():
    return render_template('index.html')

@app.route('/login', methods=['GET', 'POST'])
def login():
    if current_user.is_authenticated:
        return redirect(url_for('index'))
    form = LoginForm()
    if form.validate_on_submit():
        artist = Artist.query.filter_by(email=form.email.data).first()
        if artist is None or not artist.check_password(form.password.data):
            flash('Invalid username or password')
            return redirect(url_for('login'))
        login_user(artist, remember=form.remember_me.data)
        next_page = request.args.get('next')
        if not next_page or url_parse(next_page).netloc != '':
            next_page = url_for('index')
        return redirect(next_page)
    return render_template('login.html', title='Sign In', form=form)

@app.route('/logout')
def logout():
    logout_user()
    return redirect(url_for('index'))


@app.route('/register', methods=['GET', 'POST'])
def register():
    form = RegistrationForm()
    genres = Genre.query.all()
    form.genres.choices = [(a.id, a.genre) for a in genres]
    if current_user.is_authenticated:
        return redirect(url_for('index'))
    if form.validate_on_submit():
        new_artist = Artist(artistName=form.artistName.data, email=form.email.data, bio=form.bio.data)
        new_artist.set_password(form.password.data)
        db.session.add(new_artist)
        db.session.commit()
        flash('Congratulations, you are now a registered user!')
        #genres_in_form = []

        return redirect(url_for('login'))
    return render_template('register.html', title='Register', form=form)


#To do: have to get this route to work.
@app.route('/artist_account/<name>', methods=['GET', 'POST'])
@login_required
def artist_account(name):
    artist = Artist.query.filter_by(artistName=name).first_or_404()
    performances = [{'performances': artist.artistPerformances}]
    return render_template('artist_account.html', artist=artist, performances=performances)


#TODO: language (Artist instead of current_user) and extra fields
@app.route('/edit_profile', methods=['GET', 'POST'])
@login_required
def edit_profile():
    form = EditProfile()
    genres = Genre.query.all()
    form.genres.choices = [(a.id, a.genre) for a in genres]
    if form.validate_on_submit():
        current_user.username = form.username.data
        current_user.about_me = form.about_me.data
        db.session.commit()
        flash('Your changes have been saved.')
        return redirect(url_for('edit_profile'))
    elif request.method == 'GET':
        form.username.data = current_user.username
        form.about_me.data = current_user.about_me
    return render_template('edit_profile.html', title='Edit Profile',
                           form=form)


@app.route('/music_recommend', methods=['GET', 'POST'])
def music_recommend():
    form = RecommendationForm()
    genres = Genre.query.all()
    form.genres.choices = [(a.id, a.genre) for a in genres]
    if form.validate_on_submit():
        return redirect(url_for('music_recommend_results.html'))
    return render_template('music_recommend.html', title='Recommendations', form=form)



#format might cause some issues
@app.route('/event_sign_up', methods=['GET', 'POST'])
def event_sign_up():
    form = EventSignUp()
    if form.validate_on_submit():
        new_location = Location(location=form.location.data)
        new_performance = Performance(time=form.date.data, date=form.time.data, locationId=new_location.id)
        db.session.add(new_performance)
        db.session.commit()
        for i in form.location.data:
            new_perf = ArtistToPerformance(artistID=i, performanceID=new_performance.id)
            db.session.add(new_perf)
            db.session.commit()
        flash('Your changes have been saved.')
        return redirect(url_for('artist_account.html'))
    return render_template('event_sign_up.html', title='Even Signup', form=form)


@app.route('/map', methods=['GET', 'POST'])
def map():
    return render_template('map.html', title='Map')


@app.route('/reset_db')
def reset_db():
    flash("Resetting database: deleting old data and repopulating with dummy data")
    meta = db.metadata
    for table in reversed(meta.sorted_tables):
        print('Clear table {}'.format(table))
        db.session.execute(table.delete())
    db.session.commit()

    g = Genre(genre="Folk")
    db.session.add(g)
    g2 = Genre(genre="Rock")
    db.session.add(g2)
    g3 = Genre(genre="Pop")
    db.session.add(g3)
    g4 = Genre(genre="R&B")
    db.session.add(g4)
    g5 = Genre(genre="Indie")
    db.session.add(g5)
    g6 = Genre(genre="Hip Hop")
    db.session.add(g6)
    db.session.commit()
    return render_template("index.html")
