"""Models the database for the Roadtrips with Kids project"""

from flask_sqlalchemy import SQLAlchemy  

"""Import SQLAlchemy object from flask_sqlalchemy library and make the 
    connection to PostgreSQL"""

db = SQLAlchemy()   #create an instance of SQLAlchemy object

class User(db.Model):
    """Users of the website"""
    __tablename__ = 'users'

    user_id = db.Column(db.Integer,
                        primary_key = True,
                        autoincrement = True,
                        )
    username = db.Column(db.String(25), nullable = False)
    password = db.Column(db.String(25), nullable = False)
    email = db.Column(db.String(50), nullable = False)

    comment = db.relationship('Comment')
    rating = db.relationship('Rating')
    business_tip = db.relationship('BusinessTip')
    trip_tip = db.relationship('TripTip')
    answer = db.relationship('Answer')

    def __repr__(self):
        """Human readable data"""
        return f"<User id: {self.user_id}, \
                    username: {self.username},\
                    password: {self.password},\
                    email: {self.email}>"


class Business(db.Model):
    """Businesses table"""

    __tablename__ = 'businesses'

    business_id = db.Column(db.Integer,                 #taken from Yelp API
                            primary_key = True,
                            )
    business_name = db.Column(db.String(50), nullable = False)
    business_type = db.Columnd(db.String(5), nullable = False)
    description = db.Column(db.String(500), nullable = True)

    comment = db.relationship('Comment')
    rating = db.relationship('Rating')
    business_tip = db.relationship('BusinessTip')
       
    def __repr__(self):
        """Human readable data"""
        return f"<Business id: {self.business_id}, \
                    Business name: {self.business_name},\
                    Business type: {self.business_type},\
                    Description: {self.description}>"


class Comment(db.Model):
    """Comments of users on the businesses"""

    __tablename__ = 'comments'

    comment_id = db.Column(db.Integer,
                            primary_key = True,
                            autoincrement = True,
                            )
    user_id = db.Column(db.Integer, 
                        db.ForeignKey('users.user_id'),
                        )
    business_id = db.Column(db.Integer,
                            db.ForeignKey('businesses.business_id'),
                            )
    comment = db.Column(db.String(500), nullable = True)

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
                            primary_key = True,
                            autoincrement = True,
                            )
    user_id = db.Column(db.Integer, 
                        db.ForeignKey('users.user_id'),
                        )
    business_id = db.Column(db.Integer,
                            db.ForeignKey('businesses.business_id'),
                            )
    rating = db.Column(db.Integer, nullable = True)

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

    tip_id = db.Column(db.Integer,
                        primary_key = True,
                        autoincrement = True,
                        )
    user_id = db.Column(db.Integer,
                        db.ForeignKey('users.user_id'),
                        )
    business_id = db.Column(db.Integer,
                            db.ForeignKey('businesses.business_id'),
                            )
    business_tip = db.Column(db.String(150), nullable = True)
    
    user = db.relationship('User')
    business = db.relationship('Business')

    def __repr__(self):
        """Human readable data"""
        return f"<Tip id: {self.tip_id}, \
                    User id: {self.user_id},\
                    business id: {self.business_id},\
                    tip: {self.business_tip}>"

class TripTip(db.Model):
    """Tips on businesses given by users"""

    __tablename__ = 'trip_tips'

    tip_id = db.Column(db.Integer,
                        primary_key = True,
                        autoincrement = True,
                        )
    user_id = db.Column(db.Integer,
                        db.ForeignKey('users.user_id'),
                        )
    trip_tip = db.Column(db.String(150), nullable = True)
    
    user = db.relationship('User')
    
    def __repr__(self):
        """Human readable data"""
        return f"<Tip id: {self.tip_id}, \
                    User id: {self.user_id},\
                    tip: {self.trip_tip}>"

class Question(db.Model):
    """Questions to ask if you forget your password"""

    __tablename__ = 'questions'

    question_id = db.Column(db.Integer, 
                            primary_key = True,
                            autoincrement = True,
                            )
    question = db.Column(db.String(150), nullable = False)

    answer = db.relationship('Answer')

    def __repr__(self):
        """Human readable data"""
        return f"<Question id: {self.question_id},\
                    question: {self.question}>"


class Answer(db.Model):
    """Answers to those questions given by users"""

    __tablename__ = 'answers'

    answer_id = db.Column(db.Integer,
                            primary_key = True,
                            autoincrement = True,
                            )
    question_id = db.Column(db.Integer,
                            db.ForeignKey('questions.question_id'),
                            )
    user_id = db.Column(db.Integer,
                        db.ForeignKey('users.user_id'),
                        )
    answer = db.Column(db.String(25), nullable = False)

    question = db.relationship('Question')
    user = db.relationship('User')

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


if __name__ == '__main__':
    """For running this interactively"""

    from server import app

    db_name = 'travels'
    connect_to_db(app, db_name)

    print('Connected to database.')