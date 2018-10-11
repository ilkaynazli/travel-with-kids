from jinja2 import StrictUndefined

from flask import (Flask, render_template, redirect, request, flash, session)
from flask_debugtoolbar import DebugToolbarExtension

from model import (User, Business, Comment, Rating, BusinessTip,
                    TripTip, Question, Answer, connect_to_db, db)
from functions import test_the_password
import os
from flask import jsonify
import json
import requests



GOOGLE_MAPS = os.environ['GOOGLE_MAPS_API']
YELP = os.environ['YELP_API']

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
    
    result = test_the_password(password, password2)
    if not result[0]:
        return render_template("signup.html", 
                                error=True, 
                                message=result[1])

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
        session['user_id'] = user.user_id
        return redirect('/')

    return render_template("login.html", error=error)


@app.route("/wrong-password")
def wrong_password():
    """User forgot the password render the page to forgot_password"""
    return render_template("forgot_password.html")


@app.route("/forgot-password")
def forgot_password():
    """Get question and answer for the user login"""
    email = request.args.get('email')
    session['email'] = email
    if email is None:
        flash("This user does not exist. Please sign up here:")
        return render_template("signup.html")

    user = User.query.filter(User.email == email).first()
    question_id = db.session.query(Answer.question_id).filter(Answer.user_id == user.user_id).first()
    question = db.session.query(Question.question).filter(Question.question_id == question_id).first()
    return render_template("check_answer.html", question=question)


@app.route("/check-answer")
def check_answer():
    """Check if the answer matches to the one at the database"""
    user_email = session.get('email')

    user = User.query.filter(User.email == user_email).first()
    user_answer = db.session.query(Answer.answer).filter(Answer.user_id == user.user_id).first()
    
    answer = request.args.get('answer')

    if answer.lower() == user_answer[0].lower():
        return render_template("new_password.html")
    else:
        flash("Answers do not match please try again!")
        user = User.query.filter(User.email == user_email).first()
        question_id = db.session.query(Answer.question_id).filter(Answer.user_id == user.user_id).first()
        question = db.session.query(Question.question).filter(Question.question_id == question_id).first()
        return render_template("check_answer.html", question=question)


@app.route("/new-password", methods=["POST"])
def assign_new_password():
    """Assign a new password for the existing user"""

    password = request.form.get('password')
    password2 = request.form.get('password2')
    
    result = test_the_password(password, password2)
    if not result[0]:
        return render_template("new_password.html", 
                                error=True, 
                                message=result[1])

    user_email = session.get('email')
    user = User.query.filter(User.email == user_email).first()

    user.password = password
    db.session.commit()
    return redirect('/')


@app.route("/log-out")
def logout_user():
    """Log out user from the website and remove session from system"""

    session.pop('user_id', None)

    return redirect("/")


@app.route("/show-map")
def show_map():
    """Show map and directions"""
    start_location = request.args.get("start_location")
    end_location = request.args.get("end_location")

    return render_template("show_directions.html",
                            YOUR_API_KEY=GOOGLE_MAPS,
                            start=start_location,
                            end=end_location) 


@app.route("/get-route")
def get_route_data():
    """Get the response that has the directions info"""

    steps = request.args.get('myJSON')
    print('\n\n\n\n', steps, '\n\n\n\n\n')

    route = json.loads(steps)
    print('\n\n\n\n', route, '\n\n\n\n\n')
    # requests.get('https://api.yelp.com/v3/businesses/search', 
    #             headers={'Authorization': f"Bearer {YELP}"},
    #             params={'latitude': latitude,
    #                     'longitude': longitude,
    #                     'attributes': 'good-for-kids'})


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