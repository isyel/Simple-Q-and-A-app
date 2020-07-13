from .extensions import db

from flask_login import UserMixin

from werkzeug.security import generate_password_hash

class User(UserMixin, db.Model):
    __tablename__ = 'users'
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(50))
    email = db.Column(db.String(100), unique=True)
    password = db.Column(db.String)
    expert = db.Column(db.Boolean)
    admin = db.Column(db.Boolean)
    
    questions_asked = db.relationship('Question', foreign_keys='Question.asked_by_id', 
                                      backref='asker', lazy=True)
    answers_requested = db.relationship('Question', foreign_keys='Question.expert_id', 
                                      backref='expert', lazy=True)
    
    @property
    def unhashed_password():
        raise AttributeError("Cannot view unhashed password")
    
    @unhashed_password.setter
    def unhashed_password(self, unhashed_password):
        self.password = generate_password_hash(unhashed_password)
    

class Question(db.Model):
    __tablename__ = 'questions'
    id = db.Column(db.Integer, primary_key=True)
    question = db.Column(db.Text)
    answer = db.Column(db.Text)
    asked_by_id = db.Column(db.Integer, db.ForeignKey('users.id'))
    expert_id = db.Column(db.Integer, db.ForeignKey('users.id'))