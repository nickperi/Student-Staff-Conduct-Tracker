from App.models.course import Course
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

def get_all_courses_json():
    courses = Course.query.all()
    if not courses:
        return []
    courses = [course.get_json() for course in courses]
    return courses
