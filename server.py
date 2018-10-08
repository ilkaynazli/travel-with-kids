from jinja2 import StrictUndefined

from flask import (Flask, render_template, redirect, request, flash, session)
from flask_debugtoolbar import DebugToolbarExtension

from model import (User, Business, Comment, Rating, BusinessTip,
                    TripTip, Question, Answer, connect_to_db, db)

app = Flask(__name__)

# Required to use Flask sessions and the debug toolbar
app.secret_key = "ABC"

# Normally, if you use an undefined variable in Jinja2, it fails
# silently. This is horrible. Fix this so that, instead, it raises an
# error.
app.jinja_env.undefined = StrictUndefined

@app.route("/")
def display_homepage():
    """Display homepage"""
   
    return render_template("homepage.html")

@app.route("/signup")
def display_signup():
    """Display sign up details"""

    return render_template("signup.html", error=False)


@app.route("/signup", methods=["POST"])
def get_signup_info():
    """Add user info to database"""
    password = request.form.get('password')
    password2 = request.form.get('password2')
    if password != password2:
        return render_template("signup.html", 
                                error=True, 
                                message="Passwords don't match")
    if password.isalnum():
        upper = True
        lower = True
        character = True
        for char in password:
            if char.isupper() and upper:
                upper = False
            if char.islower() and lower:
                lower = False
            if char in ['!@#$%^&*(){}[]/?'] and character:
                character = False
        if upper or lower or character:
            return render_template("signup.html", 
                                    error=True, 
                                    message="Password doesn't fit the requirements")

    username = request.form.get('username')
    email = request.form.get('email')

    user = User(username=username, password=password, email=email)
    db.session.add(user)
    db.session.commit()

    return render_template("homepage.html")


@app.route("/login")
def login_user():
    """Login user to the website"""
    username = request.args.get('username')
    password = request.args.get('password')
    user = User.query.filter(User.username == username)
    if password == user.password:
        error_message = False
    else:
        error_message = True
    return render_template("login.html", error=error_message)


if __name__ == "__main__":
    # We have to set debug=True here, since it has to be True at the
    # point that we invoke the DebugToolbarExtension
    app.debug = True
    # make sure templates, etc. are not cached in debug mode
    app.jinja_env.auto_reload = app.debug

    connect_to_db(app, 'travels')

    # Use the DebugToolbar
    DebugToolbarExtension(app)

    app.run(port=5000, host='0.0.0.0')