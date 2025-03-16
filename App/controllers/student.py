from App.models.student import Student
from App.models.upvote import Upvote
from App.models.downvote import Downvote
from App.database import db

def create_student(username, password, email):
    newstudent = Student(username=username, password=password, email=email)
    db.session.add(newstudent)
    db.session.commit()
    return newstudent

def update_upvotes(id): 
    student = get_student(id)

    if student:
        upvotes = Upvote.query.filter_by(studentid=id).count()
        downvotes = Downvote.query.filter_by(studentid=id).count()
        student.score = (upvotes*5) - (downvotes*2)
        db.session.add(student)
        return db.session.commit()
    return None

def get_student(id):
    return Student.query.get(id)

def get_all_students():
    return Student.query.all()

def get_all_students_json():
    students = Student.query.all()
    if not students:
        return []
    students = [student.get_json() for student in students]
    return students
