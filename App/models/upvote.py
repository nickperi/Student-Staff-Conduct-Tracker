from App.database import db
from sqlalchemy import ForeignKey

class Upvote(db.Model):
    __tablename__ = "upvote"
    id = db.Column(db.Integer, primary_key=True)
    staffid = db.Column(db.Integer, db.ForeignKey('staff.id'), nullable=False)
    studentid = db.Column(db.Integer, db.ForeignKey('student.id'), nullable=False)

    def __init__(self, staffid, studentid):
        self.studentid = studentid
        self.staffid = staffid

    def get_json(self):
        return {
            'id': self.id,
            'staff id': self.staffid,
            'student id': self.studentid
        }

    