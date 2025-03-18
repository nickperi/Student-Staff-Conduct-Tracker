from App.models.staff import Staff
from App.models.student import Student
from App.models.upvote import Upvote
from App.models.downvote import Downvote
from App.database import db
from App.controllers import update_upvotes
from App.controllers import get_student

def create_staff(username, password, email):
    newstaff = Staff(username=username, password=password, email=email)
    db.session.add(newstaff)
    db.session.commit()
    return newstaff

def get_staff_upvotes(id):
    students_upvoted = Upvote.query.filter_by(staffid=id)
    upvotes_made = ""
    i = 1

    if students_upvoted:
        for student_upvoted in students_upvoted:
            upvotes_made += str(i) + " " + get_student(student_upvoted.studentid).username + "\n"
            i += 1
            
    return upvotes_made
    

def get_staff_downvotes(id):
    students_downvoted = Downvote.query.filter_by(staffid=id)
    downvotes_made = ""
    i = 1
    
    if students_downvoted:
        for student_downvoted in students_downvoted:
            downvotes_made += str(i) + " " + get_student(student_downvoted.studentid).username + "\n"
            i += 1
            
    return downvotes_made
    

def create_upvote(id, studentid):
    staff = Staff.query.filter_by(id=id).first()
    student = Student.query.filter_by(id=studentid).first()
   
    if staff and student:
        new_upvote = Upvote(staffid=id, studentid=studentid)
        db.session.add(new_upvote)
        db.session.commit()
        update_upvotes(id=studentid)
        staff.upvotes_made = get_staff_upvotes(id=id)
        db.session.add(staff)
        return db.session.commit()
    return None


def create_downvote(id, studentid):
    staff = Staff.query.filter_by(id=id).first()
    student = Student.query.filter_by(id=studentid).first()

    if staff and student:
        new_downvote = Downvote(staffid=id, studentid=studentid)
        db.session.add(new_downvote)
        db.session.commit()
        update_upvotes(id=studentid)
        staff.downvotes_made = get_staff_downvotes(id=id)
        return db.session.commit()
    return None


def get_staff(id):
    return Staff.query.get(id)

def get_all_staff():
    staff = Staff.query.all()

    for s in staff:
        s.upvotes_made = get_staff_upvotes(s.id)
        s.downvotes_made = get_staff_downvotes(s.id)
        
    return staff

def get_all_staff_json():
    staff = Staff.query.all()
    if not staff:
        return []
    staff = [s.get_json() for s in staff]
    return staff
