from App.models.offering import Offering
from App.models.staff import Staff
from App.models.course import Course
from App.database import db
from flask import flash

def create_offering(staff_id, course_id, semester):
    staff = Staff.query.get(staff_id)
    course = Course.query.get(course_id)
    existing_offering = Offering.query.filter_by(staff_id=staff_id, course_id=course_id, semester=semester).first()

    if existing_offering:
        flash('Offering already exists for this staff, course, and semester combination!', 'warning')
        return None

    else:
        if staff and course and not existing_offering:
            offering = Offering(staff_id=staff_id, course_id=course_id, semester=semester)
            db.session.add(offering)
            db.session.commit()
            return offering
    return None

def get_all_offerings():
    offerings = Offering.query.all()
    return offerings

def get_all_offerings_json():
    offerings = Offering.query.all()
    if not offerings:
        return []
    offerings = [offering.to_json() for offering in offerings]
    return offerings
