from App.models.student import Student
from App.models.upvote import Upvote
from App.models.downvote import Downvote
from App.models.review import Review
from App.database import db

def create_student(username, password, email):
    newstudent = Student(username=username, password=password, email=email)
    db.session.add(newstudent)
    db.session.commit()
    return newstudent

def update_score(id): 
    student = get_student(id)
    upvotes = 0
    downvotes = 0

    if student:
        reviews = Review.query.filter_by(studentid=id)

        if reviews:
            for review in reviews:
                upvotes += review.num_upvotes
                downvotes += review.num_downvotes
            student.score = (upvotes*5) - (downvotes*2)
            db.session.add(student)
            return db.session.commit()
    return None

def get_student(id):
    return Student.query.get(id)

def get_all_students():
    students = Student.query.all()
    for student in students:
        update_score(student.id)
    return students

def get_all_students_json():
    students = Student.query.all()
    if not students:
        return []
    students = [student.get_json() for student in students]
    return students
