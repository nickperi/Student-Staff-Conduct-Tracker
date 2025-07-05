from App.database import db
from sqlalchemy import ForeignKey

class Review(db.Model):
    __tablename__ = "review"
    id = db.Column(db.Integer, primary_key=True)
    staffid = db.Column(db.Integer, db.ForeignKey('staff.id'), nullable=False)
    studentid = db.Column(db.Integer, db.ForeignKey('student.id'), nullable=False)
    text = db.Column(db.String(250))
    num_upvotes = db.Column(db.Integer, default=0)
    num_downvotes = db.Column(db.Integer, default=0)

    def __init__(self, staffid, studentid, text):
        self.staffid = staffid
        self.studentid = studentid
        self.text = text

    def get_json(self):
        return {'id': self.id, 
                'staff id': self.staffid, 
                'student id': self.studentid, 
                'review': self.text,
                'upvotes': self.num_upvotes,
                'downvotes': self.num_downvotes
                }