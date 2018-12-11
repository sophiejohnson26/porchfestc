from datetime import datetime
from flask import render_template, flash, redirect, url_for, request
from flask_login import login_user, logout_user, current_user, login_required
from werkzeug.urls import url_parse
from app import app, db
from app.forms import *
from app.models import *
from app.email import send_password_reset_email

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
    if current_user.is_authenticated:
        return redirect(url_for('index'))
    if form.validate_on_submit():
        new_artist = Artist(artistName=form.artistName.data, email=form.email.data, bio=form.bio.data, genre=form.genre.data)
        new_artist.set_password(form.password.data)
        db.session.add(new_artist)
        db.session.commit()
        flash('Congratulations, you are now a registered user!')

        return redirect(url_for('login'))
    return render_template('register.html', title='Register', form=form)


#To do: have to get this route to work.
@app.route('/my_performances/', methods=['GET', 'POST'])
@login_required
def my_perfomances():
    events = current_user.artistPerformances

    return render_template('my_performances.html', artist=current_user, event_list=events)

@app.route('/artist_account/<name>')
def artist_account(name):
    artist = Artist.query.filter_by(artistName=name).first()
    events = current_user.artistPerformances

    return render_template('artist_account.html', artist=artist, event_list=events)


@app.route('/performance_edit/<performance>', methods=['GET', 'POST'])
def performance_edit(performance):
    perf = Performance.query.filter_by(id=performance).first()
    form = EditPerfomance()
    if form.validate_on_submit():
        perf.date = form.date.data
        perf.time = form.time.data
        new_location = Location(perf.locationId)
        db.session.add(new_location)
        db.session.commit()
        perf.locationId = new_location.id
        db.session.commit()
        flash('Your changes have been saved.')
        return redirect(url_for('my_performances'))
    elif request.method == 'GET':
        form.date.data = perf.date
        form.time.data = perf.time
        form.location.data = perf.locationId
    return render_template('performance_edit.html', title='Performance Edit', form=form)


#TODO: language (Artist instead of current_user) and extra fields
@app.route('/edit_profile', methods=['GET', 'POST'])
@login_required
def edit_profile():
    form = EditProfile()
    if form.validate_on_submit():
        current_user.artistName = form.artistName.data
        current_user.bio = form.bio.data
        current_user.email = form.email.data
        current_user.genre = form.genre.data
        db.session.commit()
        flash('Your changes have been saved.')
        return redirect(url_for('edit_profile'))
    elif request.method == 'GET':
        form.artistName.data = current_user.artistName
        form.bio.data = current_user.bio
        form.email.data = current_user.email
        form.genre.data = current_user.genre

    return render_template('edit_profile.html', artist=current_user, title='Edit Profile',
                           form=form)


@app.route('/music_recommend', methods=['GET', 'POST'])
def music_recommend():
    form = RecommendationForm()
    if form.validate_on_submit():
        recs = Artist.query.filter_by(genre=form.genre.data).all()
        return render_template('music_recommend_results.html', recommended_list=recs)
    return render_template('music_recommend.html', title='Recommendations', form=form)


@app.route('/event_sign_up',  methods=['GET', 'POST'])
def event_sign_up():
    form = EventSignUp()
    if form.validate_on_submit():
        new_location = Location(location=form.location.data)
        db.session.add(new_location)
        db.session.commit()
        new_performance = Performance(time=form.time.data, date=form.date.data, locationId=new_location.id)
        db.session.add(new_performance)
        db.session.commit()
        random=ArtistToPerformance(artistID=current_user.id, performanceID=new_performance.id)
        db.session.add(random)
        db.session.commit()
        flash('Your changes have been saved.')
        return redirect(url_for('artist_account'))
    return render_template('event_sign_up.html', title='Event Signup', form=form)


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
    return render_template("index.html")


@app.route('/reset_password_request', methods=['GET', 'POST'])
def reset_password_request():
    if current_user.is_authenticated:
        return redirect(url_for('index'))
    form = ResetPasswordRequestForm()
    if form.validate_on_submit():
        current_artist = Artist.query.filter_by(email=form.email.data).first()
        if current_artist:
            send_password_reset_email(current_artist)
        flash('Check your email for the instructions to reset your password')
        return redirect(url_for('login'))
    return render_template('reset_password_request.html',
                           title='Reset Password', form=form)


@app.route('/reset_password/<token>', methods=['GET', 'POST'])
def reset_password(token):
    if current_user.is_authenticated:
        return redirect(url_for('index'))
    current_artist = Artist.verify_reset_password_token(token)
    if not current_artist:
        return redirect(url_for('index'))
    form = ResetPasswordForm()
    if form.validate_on_submit():
        current_artist.set_password(form.password.data)
        db.session.commit()
        flash('Your password has been reset.')
        return redirect(url_for('login'))
    return render_template('reset_password.html', form=form)
