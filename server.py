from jinja2 import StrictUndefined

from flask import (Flask, render_template, redirect, request, flash, session)
from flask_debugtoolbar import DebugToolbarExtension

from model import (User, Business, Comment, Rating, BusinessTip, Route, Stopover,
                    TripTip, Question, Answer, connect_to_db, db)
from functions import test_the_password, hash_password, check_hashed_password
import os
from flask import jsonify
import json
import requests
from api import get_businesses, get_business_info


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

@app.route("/show-signup-button.json", methods=['POST'])
def display_signup():
    """Display sign up details"""
    questions = Question.query.all()
    my_questions =[]
    for question in questions:
        my_questions.append({'id': question.question_id,
                            'question': question.question})
    my_response = {'questions': my_questions}
    return jsonify(my_response)


@app.route("/signup.json", methods=["POST"])
def get_signup_info():
    """Add user info to database"""
    password = request.json['password']   
    result = test_the_password(password)
    if result:
        return jsonify({'error': result})

    username = request.json['username']
    email = request.json['email']
    
    hashed_password = hash_password(password)
    user = User(username=username, password=hashed_password, email=email)

    question_id = request.json['userQuestion']
    user_answer = request.json['answer']
    answer = Answer(question_id=question_id, user=user, answer=user_answer)

    db.session.add_all([user, answer])
    db.session.commit()

    return jsonify({'error': result})


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
   
    if not check_hashed_password(password, user.password):  #if password doesn't match function returns False
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
    password = request.json['password']
    result = test_the_password(password)
    if result == False:    #if error is false
        user_email = session.get('email')
        user = User.query.filter(User.email == user_email).first()
        hashed_password = hash_password(password)
        del password
        user.password = hashed_password
        db.session.commit()

    return jsonify({'error': result})


@app.route("/log-out")
def logout_user():
    """Log out user from the website and remove session from system"""
    session.pop('user_id', None)
    return redirect("/")


@app.route("/show-map")
def show_map():
    """Show map and directions"""

    start_location = request.args.get("start_location").title()
    end_location = request.args.get("end_location").title()
    user_id = session.get('user_id')

    if user_id and Route.query.filter(Route.user_id == user_id, 
                                      Route.start == start_location, 
                                      Route.end == end_location).first() is None:
            route = Route(user_id=user_id, start=start_location, end=end_location)
            db.session.add(route)
            db.session.commit()

    my_route = Route.query.filter(Route.start == start_location,
                                  Route.end == end_location).first()
    session['route_id'] = my_route.route_id

    return render_template("show_directions.html",
                            YOUR_API_KEY=GOOGLE_MAPS,
                            start=start_location,
                            end=end_location,
                            )


@app.route("/show-markers.json")
def show_business_markers():
    """Get the response that has the directions info"""

    coordinates = json.loads(request.args.get('coordinates'))

    options = json.loads(request.args.get('categories'))    
    categories_list = options.split('&categories=')
    radius = categories_list[0].lstrip('points=')
    categories = ','.join(categories_list[1:])

    results = get_businesses(coordinates, categories, radius)
    return jsonify(results)


@app.route("/business/<business_id>")
def display_business_page(business_id):
    """Display info on a business like name, address, phone, images, url to yelp"""

    business = get_business_info(business_id)
    return render_template("businesses.html", business2=json.dumps(business), business=business, YOUR_API_KEY=GOOGLE_MAPS)


@app.route("/save-stopovers", methods=['POST'])
def save_stopovers_to_database():
    """Save the user selected stopovers to database"""

    data = request.form.get('stopover') #this is a string
    check, name = data.split('-')

    print('\n\n\n\n', check, name, '\n\n\n\n')

    business = db.session.query(Business).filter(Business.business_name == name).first()
    print('\n\n\n\n', business, '\n\n\n\n')
    print('\n\n\n\n\n', session.get('route_id'), '\n\n\n\n\n')
    route_id = session.get('route_id')
    stopover = Stopover(route_id=route_id, 
                            latitude=business.latitude, 
                            longitude=business.longitude,
                            business_id=business.business_id)

    test = Stopover.query.filter(Stopover.route_id == route_id, 
                             Stopover.business_id == business.business_id).first()
    print('\n\n\n\n', test, '\n\n\n', stopover, '\n\n\n\n')


    if check == 'remove' and test:        
        db.session.delete(test)
        db.session.commit()
        print('\n\n\ndeleted\n\n\n')
        
    if check == 'add' and test is None:
        db.session.add(stopover)
        db.session.commit()
        print('\n\n\nadded\n\n\n')

    return "The server received your request and modified the db appropriately."


@app.route("/users/<int:user_id>")
def display_user_info(user_id):
    """Display user info: Name, id, last search, favorited businesses, etc.""" 

    user = User.query.filter(User.user_id == user_id).first()

    routes_by_user = db.session.query(Route).filter(Route.user_id == user.user_id)
    my_routes = routes_by_user.order_by(Route.route_id.desc()).limit(3).all()
    print('\n\n\n\n\n', my_routes, '\n\n\n\n')

    return render_template("users.html", user=user, routes=my_routes, YOUR_API_KEY=GOOGLE_MAPS)
   
@app.route("/stopover-route/<this_route>")
def display_route_with_stopovers(this_route):
    """Show the map and route but include the stopovers"""
    start, end = this_route.split('&')
    print('\n\n\n\n', start, end, '\n\n\n\n\n')
    user_id = session.get('user_id')
    my_route = Route.query.filter(Route.start == start, Route.end == end, Route.user_id == user_id).first()
    stopovers = Stopover.query.filter(Stopover.route_id == my_route.route_id).all()
    my_stopovers = []

    for item in stopovers:
        name = db.session.query(Business.business_name).filter(Business.business_id == item.business_id).first()
        stopover = {
                    'latitude': item.latitude,
                    'longitude': item.longitude,
                    'id': item.business_id,
                    'name': name
                    }
        my_stopovers.append(stopover)

    print('\n\n\n\n', my_stopovers, '\n\n\n\n')

    my_data = {'stopovers': my_stopovers}

    return jsonify(my_data)

if __name__ == "__main__":
    # We have to set debug=True here, since it has to be True at the
    # point that we invoke the DebugToolbarExtension
    app.debug = True
    # make sure templates, etc. are not cached in debug mode
    app.jinja_env.auto_reload = app.debug

    connect_to_db(app, 'travels')

    # Use the DebugToolbar
    # DebugToolbarExtension(app)

    app.run(port=5000, host='0.0.0.0')