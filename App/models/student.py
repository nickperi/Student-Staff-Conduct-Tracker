from App.database import db
from App.models.user import User
from App.models.upvote import Upvote
from App.models.course import Course
from App.models.student_course import Student_Course
from sqlalchemy import ForeignKey


class Student(User):
    __tablename__ = "student"
    id = db.Column(db.Integer, db.ForeignKey('user.id'), primary_key=True)
    username =  db.Column(db.String, nullable=False, unique=True)
    email = db.Column(db.String(120), nullable=False)
    score = db.Column(db.Integer, default=0)
    courses = db.relationship('Course', secondary='student_course', backref=db.backref('student', lazy='dynamic'), lazy='dynamic')

    __mapper_args__ = {
        'polymorphic_identity': 'student',
    }


    def __init__(self, username, password, email):
        self.username = username
        self.set_password(password)
        self.email = email


    def get_json(self):
        return{
            'id': self.id,
            'username': self.username,
            'email': self.email,
            'score': self.score,
            'courses': [course.code + ' - ' + course.title for course in self.courses]
        }
    
    def get_user_type(self):
        return 'student'
