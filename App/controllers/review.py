from App.models.review import Review
from App.models.upvote import Upvote
from App.models.downvote import Downvote
from App.database import db

def get_review(id):
    return Review.query.get(id)

def update_upvotes(id): 
    review = get_review(id)

    if review:
        review.num_upvotes = Upvote.query.filter_by(reviewid=id).count()
        db.session.add(review)
        return db.session.commit()
    return None

def update_downvotes(id): 
    review = get_review(id)

    if review:
        review.num_downvotes = Downvote.query.filter_by(reviewid=id).count()
        db.session.add(review)
        return db.session.commit()
    return None

def get_upvotes(id):
    review = get_review(id)
    return review.num_upvotes

def get_downvotes(id):
    review = get_review(id)
    return review.num_downvotes

def get_all_reviews():
    return Review.query.all()

def get_all_reviews_json():
    reviews = Review.query.all()
    if not reviews:
        return []
    reviews = [review.get_json() for review in reviews]
    return reviews