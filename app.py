#!/usr/bin/env python3
import flask
from flask import request, session, g
from flask import Flask, redirect, render_template
from flask.helpers import url_for
from flask_login.utils import login_user
from modules import login, authorization


from urllib.parse import urlparse, urljoin

def is_safe_url(target):
    ref_url = urlparse(request.host_url)
    test_url = urlparse(urljoin(request.host_url, target))
    return test_url.scheme in ('http', 'https') and \
           ref_url.netloc == test_url.netloc

app = Flask(__name__)
app.secret_key = "__SECRET_KEY"

app.config["MONGO_URI"] = "mongodb://localhost:27017/puddle?readPreference=primary&appname=MongoDB%20Compass&directConnection=true&ssl=false"

User = login.User, login

login_manager = login.Login(app)
login_manager.session_protection = "strong"

auth = authorization.Auth(app)
sess = authorization.Sessions(app)

@app.before_request
def before_request():
    g.user = None

    session.pop('_flashes', None)

    if '_sessionId' in session:
        user = sess.getUserFromSession(session["_sessionId"])
        if user:
            g.user = User(user)

        else:
            session.pop('_sessionId',None)
            

@app.route('/login', methods=['GET','POST'])
def login():
    error = None
    if request.method == 'POST':
        session.pop("_sessionId",None)

        email, password = request.form.get('email'), request.form.get('password')

        user = auth.get_user(email)
        if user != None and auth.validate_user(user, password) == True:

            __SESSION_ID = sess.newSession(user['_id'])
            session['_sessionId'] = __SESSION_ID

            g.user = User(user)

            flask.flash(f"Logged in successfully.")

            next = flask.request.args.get('next')
            if not is_safe_url(next):
                return flask.abort(400)

            return flask.redirect(url_for(next or 'profile'))
        else:

            flask.flash("Could not find user with these credentials.")

    return render_template('login.html')

@app.route('/logout',methods=['GET'])
def logout():
    if g.user != None:

        sess.deleteSession(session["_sessionId"])

        g.user = None

        session.pop("_sessionId",None)

        flask.flash("Logged out.")

    return flask.redirect(url_for("login"))

@app.route('/register',methods=['GET','POST'])
def register():
    error = None
    if request.method == 'POST':
        session.pop("_sessionId",None)

        email, password = request.form.get('email'), request.form.get('password')

        user = auth.get_user(email)
        if user == None:
            auth.registerUser(email, password)

            return flask.redirect(url_for('login'))

        else:

            flask.flash("Email already registered.")

    return render_template('register.html')

@app.route('/profile',methods=['GET','POST'])
def profile():
    if not g.user:
        return redirect(url_for('login'))

    return render_template('profile.html')

app.run()