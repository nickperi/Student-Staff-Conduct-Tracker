from App.database import db
from App.models.user import User
from App.models.upvote import Upvote
from sqlalchemy import ForeignKey

class Student(User):
    __tablename__ = "student"
    id = db.Column(db.Integer, db.ForeignKey('user.id'), primary_key=True)
    username =  db.Column(db.String, nullable=False, unique=True)
    email = db.Column(db.String(120), nullable=False)
    num_upvotes = db.Column(db.Integer, default=0)
    score = db.relationship('Upvote', backref='student', lazy=True)

    __mapper_args__ = {
        'polymorphic_identity': 'student',
    }


    def __init__(self, username, password, email):
        self.username = username
        self.set_password(password)
        self.email = email

    def staff_list(self):
        upvotes = Upvote.query.filter_by(studentid=self.id)



    def get_json(self):
        return{
            'id': self.id,
            'username': self.username,
            'email': self.email,
            'score': self.score
        }
    
    def get_user_type(self):
        return 'student'
