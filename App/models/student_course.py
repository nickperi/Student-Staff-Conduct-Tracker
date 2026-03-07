from App.database import db
from sqlalchemy import ForeignKey

class Student_Course(db.Model):
    __tablename__ = 'student_course'
    student_id = db.Column(db.Integer, db.ForeignKey('student.id'), primary_key=True)
    course_id = db.Column(db.Integer, db.ForeignKey('course.id'), primary_key=True)

def __init__(self, student_id, course_id):
    self.student_id = student_id
    self.course_id = course_id

def to_json(self):
    return {
        'student_id': self.student_id,
        'course_id': self.course_id
    }

