from App.database import db
from sqlalchemy import ForeignKey

class Enrollment(db.Model):
    __tablename__ = 'enrollment'
    student_id = db.Column(db.Integer, db.ForeignKey('student.id'), primary_key=True)
    offering_id = db.Column(db.Integer, db.ForeignKey('offering.id'), primary_key=True)

def __init__(self, student_id, offering_id):
    self.student_id = student_id
    self.offering_id = offering_id

def to_json(self):
    return {
        'student_id': self.student_id,
        'offering_id': self.offering_id
    }

