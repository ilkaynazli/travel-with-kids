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
    username = db.Column(db.String(25), nullable = False, unique=True)
    password = db.Column(db.String(25), nullable = False)
    email = db.Column(db.String(50), nullable = False)

    comments = db.relationship('Comment')
    ratings = db.relationship('Rating')
    business_tips = db.relationship('BusinessTip')
    trip_tips = db.relationship('TripTip')
    answers = db.relationship('Answer')

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
    business_type = db.Column(db.String(5), nullable = False)
    description = db.Column(db.Text, nullable = True)

    comments = db.relationship('Comment')
    ratings = db.relationship('Rating')
    business_tips = db.relationship('BusinessTip')
       
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

    business_tip_id = db.Column(db.Integer,
                        primary_key = True,
                        autoincrement = True,
                        )
    user_id = db.Column(db.Integer,
                        db.ForeignKey('users.user_id'),
                        )
    business_id = db.Column(db.Integer,
                            db.ForeignKey('businesses.business_id'),
                            )
    business_tip = db.Column(db.Text, nullable = True)

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
                        primary_key = True,
                        autoincrement = True,
                        )
    user_id = db.Column(db.Integer,
                        db.ForeignKey('users.user_id'),
                        )
    trip_tip = db.Column(db.Text, nullable = True)
    
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
                            primary_key = True,
                            autoincrement = True,
                            )
    question = db.Column(db.String(150), nullable = False)

    answers = db.relationship('Answer')

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
    
    User.query.delete()
    Business.query.delete()
    Comment.query.delete()
    Rating.query.delete()
    BusinessTip.query.delete()
    TripTip.query.delete()
    Question.query.delete()
    Answer.query.delete()

    #add user, business, comment, rating, tips, question, answer
    sample_user = User(username='ilkay', 
                        password='12345Qwe/',
                        email='ilkay@ilkay.com')
    sample_business = Business(business_id=1, 
                                business_name='test', 
                                business_type='food')
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
                        sample_answer])
    db.session.commit()




if __name__ == '__main__':
    """For running this interactively"""

    from server import app

    db_name = 'travels'
    connect_to_db(app, db_name)

    db.create_all()
    # example_data()

    print('Connected to database.')