from App.database import db
from App.models.user import User
from App.models.upvote import Upvote
from App.models.student import Student
from sqlalchemy import ForeignKey

class Staff(User):
    __tablename__ = "staff"
    id = db.Column(db.Integer, db.ForeignKey('user.id'), primary_key=True)
    username =  db.Column(db.String, nullable=False, unique=True)
    email = db.Column(db.String(120), nullable=False)
    reviews_logged = db.relationship('Review', backref='staff', lazy='dynamic')
    upvotes_made = db.relationship('Upvote', backref='staff', lazy='dynamic')
    downvotes_made = db.relationship('Downvote', backref='staff', lazy='dynamic')


    __mapper_args__ = {
        'polymorphic_identity': 'staff'
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
            'upvotes made': self.upvotes_made,
            'downvotes made': self.downvotes_made
        }
    
    def get_user_type(self):
        return 'staff'
