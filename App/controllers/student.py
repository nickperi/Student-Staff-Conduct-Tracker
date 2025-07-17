from sqlalchemy import asc, desc
from App.controllers.review import analyze_sentiment
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
    score = 0

    if student:
        reviews = Review.query.filter_by(studentid=id)

        if reviews:

            for review in reviews:
                if(analyze_sentiment(review.text) == "Positive"):
                    score += review.num_upvotes*5
                    score -= review.num_downvotes*2
                elif(analyze_sentiment(review.text) == "Negative"):
                    score += review.num_downvotes*5
                    score -= review.num_upvotes*2
                else:
                    score += review.num_upvotes*3
                    score -= review.num_downvotes*3

            student.score = score
            db.session.add(student)
            return db.session.commit()
    return None

def get_student(id):
    return Student.query.get(id)

def get_all_students():
    students = Student.query.order_by(desc(Student.score)).all()
    for student in students:
        update_score(student.id)
    return students

def get_all_students_json():
    students = Student.query.all()
    if not students:
        return []
    students = [student.get_json() for student in students]
    return students

def sort_students_by_id(ascending):
    if ascending:
        students = Student.query.order_by(asc(Student.id)).all()
    else:
        students = Student.query.order_by(desc(Student.id)).all()

    students = [student.get_json() for student in students]
    return students


def sort_students_by_username(ascending):
    if ascending:
        students = Student.query.order_by(asc(Student.username)).all()
    else:
        students = Student.query.order_by(desc(Student.username)).all()
    students = [student.get_json() for student in students]
    return students


def sort_students_by_score(ascending):
    if ascending:
        students = Student.query.order_by(asc(Student.score)).all()
    else:
        students = Student.query.order_by(desc(Student.score)).all()
    students = [student.get_json() for student in students]
    return students