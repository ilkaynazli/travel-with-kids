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

    return render_template("signup.html", 
                            error=False,
                            questions = Question.query.all())


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

    question_id = request.form.get('question')
    user_answer = request.form.get('answer')
    answer = Answer(question_id=question_id, user=user, answer=user_answer)

    db.session.add_all([user, answer])
    db.session.commit()

    return render_template("homepage.html")


@app.route("/login")
def login_user():
    """Login user to the website"""
    username = request.args.get('username')
    password = request.args.get('password')
    user = User.query.filter(User.username == username).first()
    if user is None:
        error = False
    if password == user.password:
        error = False
    else:
        error = True
    return render_template("login.html", error=error)


@app.route("/forgot-password")
def forgot_password():
    """Get question and answer for the user login"""
    email = request.args.get('email')
    if email is None:
        flash("This user does not exist. Please sign up here")
        return render_template("signup.html")

    question = db.session.query(Question.question)
                .filter(Question.user.email == email).first()
    return render_template("check_answer.html", question=question)


@aap.route("/check-answer")
def check_answer():
    user_email = session.get('email')
    user_answer = db.session.query(Answer.answer)
                .filter(User.email == user_email).first()
    answer = request.args.get('answer')
    if answer.lower() == user_answer.lower():
        return render_template("new_password.html")
    else:
        flash("Answers do not match please try again!")
        question = db.session.query(Question.question)
                .filter(Question.user.email == email).first()
        return render_template("check_answer.html", question=question)


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