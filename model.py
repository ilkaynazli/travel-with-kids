"""Models the database for the Roadtrips with Kids project"""

from flask_sqlalchemy import SQLAlchemy  
from passlib.hash import argon2

"""Import SQLAlchemy object from flask_sqlalchemy library and make the 
    connection to PostgreSQL"""

db = SQLAlchemy()   #create an instance of SQLAlchemy object

class User(db.Model):
    """Users of the website"""
    __tablename__ = 'users'

    user_id = db.Column(db.Integer,
                        primary_key=True,
                        autoincrement=True,
                        )
    username = db.Column(db.String(25), nullable=False, unique=True)
    password = db.Column(db.String(150), nullable=False)
    email = db.Column(db.String(50), nullable=False)

    comments = db.relationship('Comment')
    ratings = db.relationship('Rating')
    business_tips = db.relationship('BusinessTip')
    trip_tips = db.relationship('TripTip')
    answers = db.relationship('Answer')
    favorites = db.relationship('Favorite')

    def __repr__(self):
        """Human readable data"""
        return f"<User id: {self.user_id}, \
                    username: {self.username},\
                    password: {self.password},\
                    email: {self.email}>"


class Business(db.Model):
    """Businesses table"""

    __tablename__ = 'businesses'

    business_id = db.Column(db.String(100),                 #taken from Yelp API
                            primary_key = True,
                            )
    business_name = db.Column(db.String(150), nullable=False)
    business_type = db.Column(db.String(5), nullable=True)
    latitude = db.Column(db.Float, nullable=False)
    longitude = db.Column(db.Float, nullable=False)


    comments = db.relationship('Comment')
    ratings = db.relationship('Rating')
    business_tips = db.relationship('BusinessTip')
    favorites = db.relationship('Favorite')
       
    def __repr__(self):
        """Human readable data"""
        return f"<Business id: {self.business_id}, \
                    Business name: {self.business_name},\
                    lat: {self.latitude},\
                    lng: {self.longitude}>"

class Favorite(db.Model):
    """Saved businesses by the user"""

    __tablename__ = 'favorites'

    favorite_id = db.Column(db.Integer,
                            primary_key=True,
                            autoincrement=True)
    user_id = db.Column(db.Integer,
                        db.ForeignKey('users.user_id'),
                        nullable=False
                        )
    business_id = db.Column(db.String(100),
                            db.ForeignKey('businesses.business_id'),
                            nullable=False
                            )
    user = db.relationship('User')
    business = db.relationship('Business')

    def __repr__(self):
        """Human readable"""
        return f"<Favorite id: {self.favorite_id},\
                    user id: {self.user_id},\
                    business id: {self.business_id}>"

class Comment(db.Model):
    """Comments of users on the businesses"""

    __tablename__ = 'comments'

    comment_id = db.Column(db.Integer,
                            primary_key=True,
                            autoincrement=True,
                            )
    user_id = db.Column(db.Integer, 
                        db.ForeignKey('users.user_id'),
                        nullable=False
                        )
    business_id = db.Column(db.String(100),
                            db.ForeignKey('businesses.business_id'),
                            nullable=False
                            )
    comment = db.Column(db.String(500), nullable=True)

    user = db.relationship('User')
    business = db.relationship('Business')

    def __repr__(self):
        """Human readable data"""
        return f"<Comment id: {self.comment_id}, \
                    User id: {self.user_id},\
                    business id: {self.business_id},\
                    comment: {self.comment}>"


class Rating(db.Model):
    """Ratings of businesses made by users"""

    __tablename__ = 'ratings'

    rating_id = db.Column(db.Integer,
                            primary_key=True,
                            autoincrement=True,
                            )
    user_id = db.Column(db.Integer, 
                        db.ForeignKey('users.user_id'),
                        nullable=False
                        )
    business_id = db.Column(db.String(100),
                            db.ForeignKey('businesses.business_id'),
                            nullable=False
                            )
    rating = db.Column(db.Integer, nullable=True)

    user = db.relationship('User')
    business = db.relationship('Business')

    def __repr__(self):
        """Human readable data"""
        return f"<Rating id: {self.rating_id}, \
                    User id: {self.user_id},\
                    business id: {self.business_id},\
                    rating: {self.rating}>"


class BusinessTip(db.Model):
    """Tips on businesses given by users"""

    __tablename__ = 'business_tips'

    business_tip_id = db.Column(db.Integer,
                        primary_key=True,
                        autoincrement=True,
                        )
    user_id = db.Column(db.Integer,
                        db.ForeignKey('users.user_id'),
                        nullable=False
                        )
    business_id = db.Column(db.String(100),
                            db.ForeignKey('businesses.business_id'),
                            nullable=False
                            )
    business_tip = db.Column(db.Text, nullable=True)

    user = db.relationship('User')
    business = db.relationship('Business')

    def __repr__(self):
        """Human readable data"""
        return f"<Tip id: {self.business_tip_id}, \
                    User id: {self.user_id},\
                    business id: {self.business_id},\
                    tip: {self.business_tip}>"

class TripTip(db.Model):
    """Tips on businesses given by users"""

    __tablename__ = 'trip_tips'

    trip_tip_id = db.Column(db.Integer,
                        primary_key=True,
                        autoincrement=True,
                        )
    user_id = db.Column(db.Integer,
                        db.ForeignKey('users.user_id'),
                        nullable=False
                        )
    trip_tip = db.Column(db.Text, nullable=True)
    
    user = db.relationship('User')

    def __repr__(self):
        """Human readable data"""
        return f"<Tip id: {self.trip_tip_id}, \
                    User id: {self.user_id},\
                    tip: {self.trip_tip}>"

class Question(db.Model):
    """Questions to ask if you forget your password"""

    __tablename__ = 'questions'

    question_id = db.Column(db.Integer, 
                            primary_key=True,
                            autoincrement=True,
                            )
    question = db.Column(db.String(150), nullable=False)

    answers = db.relationship('Answer')

    def __repr__(self):
        """Human readable data"""
        return f"<Question id: {self.question_id},\
                    question: {self.question}>"


class Answer(db.Model):
    """Answers to those questions given by users"""

    __tablename__ = 'answers'

    answer_id = db.Column(db.Integer,
                            primary_key=True,
                            autoincrement=True,
                            )
    question_id = db.Column(db.Integer,
                            db.ForeignKey('questions.question_id'),
                            nullable=False
                            )
    user_id = db.Column(db.Integer,
                        db.ForeignKey('users.user_id'),
                        nullable=False
                        )
    answer = db.Column(db.String(25), nullable=False)

    user = db.relationship('User')
    question = db.relationship('Question')

    def __repr__(self):
        """Human readable data"""
        return f"<Answer id: {self.answer_id},\
                    question id: {self.question_id},\
                    user id: {self.user_id},\
                    answer: {self.answer}>"


def connect_to_db(app, db_name):
    """Connect to database"""
    app.config['SQLALCHEMY_DATABASE_URI'] = 'postgresql:///' + db_name
    app.config['SQLALCHEMY_ECHO'] = True    #For debugging purposes keep this True
    db.app = app
    db.init_app(app)


def example_data():
    """Create example data for the test database."""

    #add user, business, comment, rating, tips, question, answer
    sample_user = User(username='ilkay', 
                        password=argon2.hash('123Qwe/'),
                        email='ilkay@ilkay.com')
    sample_business = Business(business_id='IBZbaTy-_Ds7GITu4QimHQ', 
                                business_name='Wildhaven Ranch', 
                                business_type='zoo',
                                latitude=34.256787,
                                longitude=-117.161389)
    sample_favorite = Favorite(user=sample_user,
                                business=sample_business)
    sample_comment = Comment(user=sample_user, 
                                business=sample_business,
                                comment='hi there')
    sample_rating = Rating(user=sample_user, 
                                business=sample_business,
                                rating=5)
    sample_tip_b = BusinessTip(user=sample_user, 
                                business=sample_business,
                                business_tip='bring wet towels')
    sample_tip_t = TripTip(user=sample_user,
                            trip_tip='bring toys')
    sample_question = Question(question='Favorite color?')
    sample_answer = Answer(question=sample_question,
                            user=sample_user,
                            answer='blue')


    db.session.add_all([sample_user,
                        sample_business, 
                        sample_rating, 
                        sample_comment,
                        sample_tip_b,
                        sample_tip_t,
                        sample_question,
                        sample_answer,
                        sample_favorite])
    db.session.commit()


db_name = 'travels'

if __name__ == '__main__':
    """For running this interactively"""

    from server import app


    connect_to_db(app, db_name)

    db.create_all()
    # example_data()

    print('Connected to database.')