from App.models.staff import Staff
from App.models.student import Student
from App.models.review import Review
from App.models.upvote import Upvote
from App.models.downvote import Downvote
from App.database import db

from App.controllers import update_upvotes
from App.controllers import update_downvotes
from App.controllers import get_student
from App.controllers import get_review

def create_staff(username, password, email):
    newstaff = Staff(username=username, password=password, email=email)
    db.session.add(newstaff)
    db.session.commit()
    return newstaff
    
def log_review(id, studentid, text):
    staff = Staff.query.filter_by(id=id).first()
    student = Student.query.filter_by(id=studentid).first()

    if staff and student:
        new_review = Review(staffid=id, studentid=studentid, text=text)
        db.session.add(new_review)
        db.session.commit()
        return db.session.commit()
    return None


def create_upvote(id, reviewid):
    review = Review.query.filter_by(id=reviewid).first()
    existing_upvote = Upvote.query.filter_by(staffid=id, reviewid=reviewid).first()
    existing_downvote = Downvote.query.filter_by(staffid=id, reviewid=reviewid).first()

    if existing_downvote:
        remove_downvote(id, reviewid)

    if not existing_upvote:
        new_upvote = Upvote(staffid=id, reviewid=reviewid)
        db.session.add(new_upvote)
        review.num_upvotes += 1
        db.session.commit()
        return new_upvote
    return None

def remove_upvote(id, reviewid):
    upvote = Upvote.query.filter_by(staffid=id, reviewid=reviewid).first()
    review = Review.query.filter_by(id=reviewid).first()

    if upvote and review:
        db.session.delete(upvote)
        review.num_upvotes -= 1
        db.session.commit()
        return upvote
    return None


def create_downvote(id, reviewid):
    staff = Staff.query.filter_by(id=id).first()
    review = Review.query.filter_by(id=reviewid).first()
    existing_downvote = Downvote.query.filter_by(staffid=id, reviewid=reviewid).first()
    existing_upvote = Upvote.query.filter_by(staffid=id, reviewid=reviewid).first()

    if existing_upvote:
        remove_upvote(id, reviewid)

    if not existing_downvote:
        new_downvote = Downvote(staffid=id, reviewid=reviewid)
        db.session.add(new_downvote)
        review.num_downvotes += 1
        return db.session.commit()
    return None


def remove_downvote(id, reviewid):
    downvote = Downvote.query.filter_by(staffid=id, reviewid=reviewid).first()
    review = Review.query.filter_by(id=reviewid).first()

    if downvote and review:
        db.session.delete(downvote)
        review.num_downvotes -= 1
        db.session.commit()
        return downvote
    return None


def get_staff(id):
    return Staff.query.get(id)

def get_staff_reviews(id):
    staff = get_staff(id)
    return staff.reviews_logged.order_by(Review.id.desc()).all()

def get_all_staff():
    staff = Staff.query.all()
    return staff

def get_all_staff_json():
    staff = Staff.query.all()
    if not staff:
        return []
    staff = [s.get_json() for s in staff]
    return staff
