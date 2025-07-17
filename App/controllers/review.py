from App.models.review import Review
from App.models.upvote import Upvote
from App.models.downvote import Downvote
from App.database import db
from datetime import datetime
from textblob import TextBlob

def get_review(id):
    return Review.query.get(id)


def analyze_sentiment(text):
    polarity = TextBlob(text).sentiment.polarity
    if polarity > 0.1:
        return "Positive"
    elif polarity < -0.1:
        return "Negative"
    else:
        return "Neutral"
    

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

def calculate_time_elapsed(dt):
    diff = datetime.now() - dt
    seconds = diff.total_seconds()

    if(seconds < 60):
        return f"{int(seconds)}s"
    elif(seconds < 3600):
        return f"{int(seconds//60)}m"
    elif(seconds < 86400):
        return f"{int(seconds//3600)}h"
    elif(seconds < 604800):
        return f"{int(seconds//86400)}d"
    elif(seconds < 2419200):
        return f"{int(seconds//604800)}w"
    else:
        return f"{diff}"

def get_all_reviews():
    return Review.query.order_by(Review.id.desc()).all()

def get_all_reviews_json():
    reviews = Review.query.all()
    if not reviews:
        return []
    reviews = [review.get_json() for review in reviews]
    return reviews
