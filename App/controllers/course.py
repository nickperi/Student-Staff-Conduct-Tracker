from App.models.course import Course
from App.models.enrollment import Enrollment
from App.models.offering import Offering
from App.controllers.student import get_student
from App.database import db

def add_course(code, title):
    course = Course(code=code, title=title)
    db.session.add(course)
    db.session.commit()
    return course


def get_course(id):
    return Course.query.get(id)

def get_all_courses():
    courses = Course.query.all()
    return courses

def get_course_offerings(course_id):
    course = get_course(course_id)
    if course:
        offerings = Offering.query.filter_by(course_id=course_id).all()
        return offerings
    return None

def get_students_in_course(course_id):
    course = Course.query.get(course_id)
    if course:
        offerings = Offering.query.filter_by(course_id=course_id).all()
        students = []

        for offering in offerings:
            enrollments = Enrollment.query.filter_by(offering_id=offering.id).all()
            students += [get_student(enrollment.student_id).username for enrollment in enrollments]
        return students
    return None

def get_all_courses_json():
    courses = Course.query.all()
    if not courses:
        return []
    courses = [course.get_json() for course in courses]
    return courses
