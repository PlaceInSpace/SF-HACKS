from flask import Blueprint, render_template, request, Flask,redirect,url_for
from flask_login import login_user, logout_user, login_required, current_user
from .models import User,tuser
from . import db
from werkzeug.security import generate_password_hash, check_password_hash

tviews = Blueprint("tviews", __name__)





#AUTH code

@tviews.route("/t/login", methods=["GET", "POST"])
def login():
  return render_template("login.html")


@tviews.route("/t/signup", methods=["GET", "POST"])
def signup():
  if request.method == "POST":
    email = request.form.get("email")
    username = request.form.get("username")
    password1 = request.form.get("password")

    email_exists = tuser.query.filter_by(email=email).first()
    username_exists = tuser.query.filter_by(username=username).first()
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
      new_user = tuser(email=email, username=username, password=generate_password_hash(password1, method='sha256'))
      db.session.add(new_user)
      db.session.commit()
      login_user(new_user, remember=True)
      return redirect(url_for('views.home'))
  return render_template("signup.html")

# Viewing a user's calendar page
@tviews.route('/calendar/<userid>') # idk the syntax in Flask
@login_required 
def view_calendar(userid):
  """View a user's calendar on this page."""
  # do we have/need a calendar widget or something
  return render_template("index.html")


@tviews.route("/make_code")
@login_required
def make_code():
  x= f"https://sf-hacks.subscribe2.repl.co/join/{current_user.id}"
  return f"Give your patient to go to {x} to sign up"
  
  
  
# Viewing all users page
@tviews.route('/see_users')
@login_required 
def view_users():
  """View all users on this page."""
  users = Tuser.query.filter()
  return render_template("index.html", users=users)

# Chat with a user page
@tviews.route('/chat/<userid>')
@login_required 
def chat():
  """Chat with a user on this page."""
  return render_template("index.html")


