from app import app
from flask_sqlalchemy import SQLAlchemy
from sqlalchemy import event
from werkzeug.security import generate_password_hash,check_password_hash

db=SQLAlchemy(app)


class Admin(db.Model):
    id=db.Column(db.Integer,primary_key=True)
    username=db.Column(db.String(120),nullable=False)
    passhash=db.Column(db.String(256),nullable=False)

class User(db.Model):
    id=db.Column(db.Integer,primary_key=True)
    username=db.Column(db.String(120),unique=True,nullable=False)
    passhash=db.Column(db.String(256),nullable=False)
    Full_Name=db.Column(db.String(150),nullable=False)
    Qualification=db.Column(db.String(250))
    DOB=db.Column(db.Date,nullable=False)

    scores=db.relationship('Scores',backref='user',lazy=True,cascade="all, delete-orphan", passive_deletes=True)

class Subject(db.Model):
    id=db.Column(db.Integer,primary_key=True)
    Name=db.Column(db.String(256),nullable=False)
    Description=db.Column(db.String(500),nullable=False)

    chapters=db.relationship('Chapter',backref='subject',lazy=True,cascade="all, delete-orphan", passive_deletes=True)

class Chapter(db.Model):
    id=db.Column(db.Integer,primary_key=True)
    subject_id=db.Column(db.Integer,db.ForeignKey('subject.id',ondelete="CASCADE"),nullable=False)
    Name=db.Column(db.String(256),nullable=False)
    Description=db.Column(db.String(500),nullable=False)

    quizzes=db.relationship('Quiz',backref='chapter',lazy=True,cascade="all, delete-orphan", passive_deletes=True)

class Quiz(db.Model):
    id=db.Column(db.Integer,primary_key=True)
    chapter_id=db.Column(db.Integer,db.ForeignKey('chapter.id',ondelete="CASCADE"),nullable=False)
    date_of_quiz=db.Column(db.Date,nullable=False)
    time_duration=db.Column(db.String(5),nullable=False)
    Remarks=db.Column(db.String(500))
    total_marks=db.Column(db.Integer)
    Qualifying_marks=db.Column(db.Integer,nullable=False)

    questions=db.relationship('Questions',backref='quiz',lazy=True,cascade="all, delete-orphan", passive_deletes=True)
    scores=db.relationship('Scores',backref='quiz',lazy=True,cascade="all, delete-orphan", passive_deletes=True)

class Questions(db.Model):
    id=db.Column(db.Integer,primary_key=True)
    quiz_id=db.Column(db.Integer,db.ForeignKey('quiz.id',ondelete="CASCADE"),nullable=False)
    question_statement=db.Column(db.String(1000),nullable=False)
    Option_1=db.Column(db.String(500),nullable=False)
    Option_2=db.Column(db.String(500),nullable=False)
    Option_3=db.Column(db.String(500),nullable=False)
    Option_4=db.Column(db.String(500),nullable=False)
    Answer_option_no=db.Column(db.Integer,nullable=False)
    Answer=db.Column(db.String(500),nullable=False)

class Scores(db.Model):
    id=db.Column(db.Integer,primary_key=True)
    quiz_id=db.Column(db.Integer,db.ForeignKey('quiz.id',ondelete="CASCADE"),nullable=False)
    user_id=db.Column(db.Integer,db.ForeignKey('user.id',ondelete="CASCADE"),nullable=False)
    total_scored=db.Column(db.Integer,nullable=False)
    is_passed=db.Column(db.Boolean)

with app.app_context():
    @event.listens_for(db.engine, "connect")
    def enable_foreign_keys(dbapi_connection, connection_record):
        cursor = dbapi_connection.cursor()
        cursor.execute("PRAGMA foreign_keys=ON")
        cursor.close()
    
    db.create_all()

    #creating admin because Admin is predefined, no registration allowed
    admin=Admin.query.first()
    if not admin:
        passhash=generate_password_hash('admin12')
        admin=Admin(username='adminhema@gmail.com',passhash=passhash)
        db.session.add(admin)
        db.session.commit()