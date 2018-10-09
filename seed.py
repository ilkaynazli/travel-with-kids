"""Get data into the database from static files"""
from sqlalchemy import func
from model import Question
from model import connect_to_db, db, db_name
from server import app

def load_questions():
    """Load questions from questions.txt into database."""

    print("Loading questions")

    # Delete all rows in table, so if we need to run this a second time,
    # we won't be trying to add duplicate questions
    Question.query.delete()

    # Read the file and insert data one by one
    for row in open("data/questions.txt"):
        row = row.rstrip()
        question = Question(question=row)   
        db.session.add(question)

    db.session.commit()

if __name__=='__main__':
    connect_to_db(app, db_name)

    # In case tables haven't been created, create them
    db.create_all()

    load_questions()