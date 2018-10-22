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
from api import get_businesses, get_playground_info


GOOGLE_MAPS = os.environ['GOOGLE_MAPS_API']

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
    if result:
        return render_template("signup.html", 
                                error=True, 
                                )

    username = request.form.get('username')
    email = request.form.get('email')

    user = User(username=username, password=password, email=email)

    question_id = request.form.get('question')
    user_answer = request.form.get('answer')
    answer = Answer(question_id=question_id, user=user, answer=user_answer)

    db.session.add_all([user, answer])
    db.session.commit()

    return redirect('/')


@app.route("/login.json", methods=['POST'])    
def login_user():
    """Login user to the website"""
    
    data_dict = request.json
    username = data_dict.get('username')
    password = data_dict.get('password')

    user = User.query.filter(User.username == username).first()

    if user is None:
        my_response = {
                        'user_id': None,
                        'error': True
                        }
        return jsonify(my_response) 
   
    if password != user.password:
        my_response = {
                        'user_id': None,
                        'error': True
                        }
        return jsonify(my_response)

    session['user_id'] = user.user_id
    my_response = {
                    'user_id': user.user_id,
                    'error': False
                    }
    return jsonify(my_response) 

# @app.route("/forgot-password")              #I do not know how to do this yet!
# def display_email_form():
#     """Display the email request form for password recovery"""
#     return render_template("")


@app.route("/forgot-password.json", methods=['POST'])
def forgot_password():
    """Get question and answer for the user login"""
    email = request.json['email']
    user = User.query.filter(User.email == email).first()

    if user is None:
        my_response = {'question': None}
        return jsonify(my_response)

    session['email'] = email
    question_id = db.session.query(Answer.question_id).filter(Answer.user_id == user.user_id).first()
    question = db.session.query(Question.question).filter(Question.question_id == question_id).first()
    my_response = {'question': question[0]}
    return jsonify(my_response)


@app.route("/check-answer.json", methods=['POST'])
def check_answer():
    """Check if the answer matches to the one at the database"""
    user_email = session.get('email')

    user = User.query.filter(User.email == user_email).first()
    user_answer = db.session.query(Answer.answer).filter(Answer.user_id == user.user_id).first()
    
    answer = request.json['answer']
    if answer.lower() == user_answer[0].lower():
        my_response = {'error': False, 'username': user.username}
        return jsonify(my_response)
    else:
        my_response = {'error': True, 'username': ''}
        return jsonify(my_response)


@app.route("/new-password.json", methods=["POST"])
def assign_new_password():
    """Assign a new password for the existing user"""
    user_email = session.get('email')
    user = User.query.filter(User.email == user_email).first()

    password = request.json['password']
    password2 = request.json['password2']
    print('\n\n\n\n\n\n', password, '\n\n\n\n\n\n')
    print('\n\n\n\n\n\n', password2, '\n\n\n\n\n\n')

    result = test_the_password(password, password2)
    if result == False:    #if error is false
        user_email = session.get('email')
        user = User.query.filter(User.email == user_email).first()

        user.password = password
        db.session.commit()
    my_response = {'error': result,
                    }
    return jsonify(my_response)


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
    options = []
    food1 = request.args.get('food1')
    if food1 is not None:
        options.append(food1)

    food2 = request.args.get('food2')
    if food2 is not None:
        options.append(food2)

    food3 = request.args.get('food3')
    if food3 is not None:
        options.append(food3)

    food4 = request.args.get('food4')
    if food4 is not None:
        options.append(food4)

    food5 = request.args.get('food5')
    if food5 is not None:
        options.append(food5)

    food6 = request.args.get('food6')
    if food6 is not None:
        options.append(food6)

    play1 = request.args.get('play1')
    if play1 is not None:
        options.append(play1)
        
    play2 = request.args.get('play2')
    if play2 is not None:
        options.append(play2)

    play3 = request.args.get('play3')
    if play3 is not None:
        options.append(play3)

    play4 = request.args.get('play4')
    if play4 is not None:
        options.append(play4)

    play5 = request.args.get('play5')
    if play5 is not None:
        options.append(play5)

    play6 = request.args.get('play6')
    if play6 is not None:
        options.append(play6)    

    print('\n\n\n\n\n', options, '\n\n\n\n\n')
    categories = ','.join(options)
    print('\n\n\n\n\n', categories, type(categories), '\n\n\n\n\n')

    return render_template("show_directions.html",
                            YOUR_API_KEY=GOOGLE_MAPS,
                            start=start_location,
                            end=end_location,
                            options=categories) 


@app.route("/get-route.json")
def get_route_data():
    """Get the response that has the directions info"""

    steps = request.args.get('myJSON')
    coordinates = json.loads(steps)
    options = request.args.get('categories')
    print('\n\n\n\n', options, '\n\n\n\n')
    categories = json.loads(options)
    
    results = get_businesses(coordinates, categories)

    for result in results:
        if Business.query.filter(Business.business_id == result.get('business_id')).first():
            continue
        else:
            business_id = result.get('business_id')
            business_type = result.get('type')
            name = result.get('name')
            coords = result.get('coords')
            lat = coords['latitude']
            lng = coords['longitude']
            business = Business(business_id=business_id,
                                business_type=business_type,
                                business_name=name,
                                latitude=lat,
                                longitude=lng)
            db.session.add(business)
            db.session.commit()    

    return jsonify(results)

@app.route("/business/<business_id>")
def display_business_page(business_id):
    """Display info on a business like name, address, phone, images, url to yelp"""

    playground = get_playground_info(business_id)

    return render_template("businesses.html", business=playground)


@app.route("/users/<int:user_id>")
def display_user_info(user_id):
    """Display user info: Name, id, last search, favorited businesses, etc.""" 

    user = User.query.filter(User.user_id == user_id).first()

    return render_template("users.html", user=user)
   

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