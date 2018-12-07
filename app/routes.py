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
        artist = Artist.query.filter_by(artist=form.name.data).first()
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
    if current_user.is_authenticated:
        return redirect(url_for('index'))
    form = RegistrationForm()
    if form.validate_on_submit():
        artist_account.set_password(form.password.data)
        db.session.add(artist_account)
        db.session.commit()
        flash('Congratulations, you are now a registered user!')
        return redirect(url_for('login'))
    return render_template('register.html', title='Register', form=form)


@app.route('/artist_account/<name>')
@login_required
def artist_account(name):
    artist = Artist.query.filter_by(name=name).first_or_404()
    performances = [{'performances': artist.artistPerformances}]
    return render_template('artist_account.html', artist=artist, performances=performances)


#TODO: language (Artist instead of current_user) and extra fields
@app.route('/edit_profile', methods=['GET', 'POST'])
@login_required
def edit_profile():
    form = EditProfile()
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


@app.route('/music_reccomend', methods=[ 'POST'])
def music_recommend():
    form = RecommendationForm() #cant work without prepopulated table
    if form.validate_on_submit():
        return  redirect(url_for('music_recommend_results.html')) #template does not exist yet
    return render_template('music_recommend.html', title='Reccomendations', form=form)


#format might cause some issues
@app.route('/event_sign_up', methods=['GET', 'POST'])
def event_sign_up():
    form = event_sign_up()
    if form.validate_on_submit():
        new_performance = Performance(time=form.date.data, date=form.time.data, locationId=form.location.data)
        db.session.add(new_performance)
        db.session.commit()
        flash('Your changes have been saved.')
        return redirect(url_for('artist_account.html'))
    return render_template('event_sign_up.html', title='Even Signup', form=form)

def map():
    return render_template('map.html', title='Map')
