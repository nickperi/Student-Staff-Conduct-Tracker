from App.models.student import Student
from App.models.offering import Offering
from App.models.enrollment import Enrollment
from App.controllers.course import get_students_in_course
from App.database import db
from flask import flash

def enroll(student_id, offering_id):
    student = Student.query.get(student_id)
    offering = Offering.query.get(offering_id)
    exists = Enrollment.query.filter_by(student_id=student_id, offering_id=offering_id).first() is not None
    student_course_enrollment = check_student_course_enrollment(student_id, offering.course_id) # Check if student is already enrolled in the course through another offering

    if exists or student_course_enrollment:
        flash('Student is already enrolled in course!', 'warning')
        return None

    else:
        if student and offering:
            enrollment = Enrollment(student_id=student_id, offering_id=offering_id)
            db.session.add(enrollment)
            db.session.commit()
            return enrollment
        return None
    return None

def check_student_course_enrollment(student_id, course_id):
    students = get_students_in_course(course_id)
    student = Student.query.get(student_id)
    if student and students:
        return student.username in students
    return False

def get_all_enrollments():
    enrollments = Enrollment.query.all()
    return enrollments

def get_all_enrollments_json():
    enrollments = Enrollment.query.all()
    if not enrollments:
        return []
    enrollments = [enrollment.get_json() for enrollment in enrollments]
    return enrollments