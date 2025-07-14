from App.database import db
from sqlalchemy import ForeignKey
from datetime import datetime

class Review(db.Model):
    __tablename__ = "review"
    id = db.Column(db.Integer, primary_key=True)
    staffid = db.Column(db.Integer, db.ForeignKey('staff.id'), nullable=False)
    studentid = db.Column(db.Integer, db.ForeignKey('student.id'), nullable=False)
    text = db.Column(db.String(250))
    upvotes = db.relationship('Upvote', backref='review', lazy='dynamic')
    downvotes = db.relationship('Downvote', backref='review', lazy='dynamic')
    num_upvotes = db.Column(db.Integer, default=0)
    num_downvotes = db.Column(db.Integer, default=0)
    created_at = db.Column(db.DateTime, default=datetime.now)
    updated_at = db.Column(db.DateTime, default=datetime.now, onupdate=datetime.now)

    def __init__(self, staffid, studentid, text):
        self.staffid = staffid
        self.studentid = studentid
        self.text = text

    def get_json(self):
        return {'id': self.id, 
                'staffid': self.staffid, 
                'studentid': self.studentid, 
                'text': self.text,
                'num_upvotes': self.num_upvotes,
                'num_downvotes': self.num_downvotes
                }
