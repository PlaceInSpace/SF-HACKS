from flask import Blueprint, render_template, request, Flask,redirect,url_for
from flask_login import login_user, logout_user, login_required, current_user
from .models import User, Post
from . import db
from werkzeug.security import generate_password_hash, check_password_hash
from datetime import datetime

views = Blueprint("views", __name__)

#AUTH code

@views.route("/login", methods=["GET", "POST"])
def login():
  if request.method == 'POST':
    email = request.form.get("email")
    password = request.form.get("password")

    user_exists = User.query.filter_by(email=email).first()

    if user_exists:
      if check_password_hash(user_exists.password, password):
        login_user(user_exists, remember=True)
        return redirect(url_for('views.home'))
      else:
        return "password or email incorrect"
    else:
      return "password or email incorrect"
  return render_template("signin.html")


@views.route("/signup", methods=["GET", "POST"])
def signup():
  if request.method == "POST":
    email = request.form.get("email")
    username = request.form.get("username")
    password1 = request.form.get("password1")

    email_exists = User.query.filter_by(email=email).first()
    username_exists = User.query.filter_by(username=username).first()
    if email_exists:
      return 'This email exists'
    elif username_exists:
      return "this username exists"
    elif len(username) < 2:
      return "this username is too short"
    elif len(password1) < 2:
      return "this pasword is too short"
    elif len(email) < 4:
      return "Email is invalid"
    else:
      new_user = User(email=email, username=username, password=generate_password_hash(password1, method='sha256'))
      db.session.add(new_user)
      db.session.commit()
      login_user(new_user, remember=True)
      return redirect(url_for('views.home'))
  return render_template("signup.html")


@views.route('/')
def begin():
  return render_template("index.html")

#dashboard for doing stuff
@views.route('/home')
def home():
  return render_template("index.html")

# About page
@views.route('/about')
def about():
  return render_template("index.html")

# Contact Us page
@views.route('/contact-us')
def contact():
  return render_template("index.html")


@views.route('/join/<code>')
@login_required
def join(code):
  user = User.query.filter_by(id=current_user).first()
  setattr(user, 't',code)
  
  return "You have joined the user as a pacient."



  
# Register a new log page
@views.route('/new-log')
@login_required 
def add_log():
  """Add a new emotion log on this page."""
  # how do you get the active user of whatever session it is?
  if request.method == 'POST':
    mood = request.form.get("mood")
    log = Post(text=mood, date_created=datetime.now(), author=current_user)
    db.session.add(log)
    db.session.commit()

  return render_template("index.html")

# Viewing all logs page
@views.route('/logs', methods=["GET", "POST"])
def view_logs():
  """View the logs overall on this page."""
  posts = Post.objects.filter(Post.author == db.session.query(User).filter(User.id == 1).first())
  return render_template("index.html", posts=posts)


