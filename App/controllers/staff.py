from App.models.staff import Staff
from App.models.student import Student
from App.models.upvote import Upvote
from App.database import db
from App.controllers import update_upvotes

def create_staff(username, password, email):
    newstaff = Staff(username=username, password=password, email=email)
    db.session.add(newstaff)
    db.session.commit()
    return newstaff


def create_upvote(id, studentid):
    staff = Staff.query.filter_by(id=id).first()
    student = Student.query.filter_by(id=studentid).first()

    if staff and student:
        new_upvote = Upvote(staffid=id, studentid=studentid)
        db.session.add(new_upvote)
        db.session.commit()
        staff.upvotes_made += 1
        update_upvotes(id=studentid)
        db.session.add(staff)
        return db.session.commit()
        
    return None


def get_staff(id):
    return Staff.query.get(id)

def get_all_staff():
    return Staff.query.all()

def get_all_staff_json():
    staff = Staff.query.all()
    if not staff:
        return []
    staff = [s.get_json() for s in staff]
    return staff