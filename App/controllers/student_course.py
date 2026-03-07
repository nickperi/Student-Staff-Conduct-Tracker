from App.models.student import Student
from App.models.course import Course
from App.models.student_course import Student_Course
from App.database import db
from flask import flash

def enroll(student_id, course_id):
    student = Student.query.get(student_id)
    course = Course.query.get(course_id)
    exists = Student_Course.query.filter_by(student_id=student_id, course_id=course_id).first() is not None

    if exists:
        flash('Student is already enrolled in course!', 'warning')
        return None

    else:
        if student and course:
            enrollment = Student_Course(student_id=student_id, course_id=course_id)
            db.session.add(enrollment)
            db.session.commit()
            return enrollment
        return None
    return None

def get_all_enrollments():
    enrollments = Student_Course.query.all()
    return enrollments

def get_all_enrollments_json():
    enrollments = Student_Course.query.all()
    if not enrollments:
        return []
    enrollments = [enrollment.get_json() for enrollment in enrollments]
    return enrollments