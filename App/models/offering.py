from App.database import db
from sqlalchemy import ForeignKey
from App.models.staff import Staff
from App.models.course import Course

class Offering(db.Model):
    __tablename__ = 'offering'
    id = db.Column(db.Integer, primary_key=True)
    staff_id = db.Column(db.Integer, db.ForeignKey('staff.id'), nullable=False)
    course_id = db.Column(db.Integer, db.ForeignKey('course.id'), nullable=False)
    semester = db.Column(db.String(20), nullable=False)

    def __init__(self, staff_id, course_id, semester):
        self.staff_id = staff_id
        self.course_id = course_id
        self.semester = semester

    def to_json(self):
        return {
            'id': self.id,
            'staff_id': self.staff_id,
            'course_id': self.course_id,
            'semester': self.semester
        }   
