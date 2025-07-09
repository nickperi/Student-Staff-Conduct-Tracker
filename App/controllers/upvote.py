from App.models.upvote import Upvote
from App.database import db

def get_upvote(id):
    return Upvote.query.get(id)

def get_my_upvotes(staffid):
    my_upvotes = Upvote.query.filter_by(staffid=staffid)
    my_upvotes = [my_upvote.reviewid for my_upvote in my_upvotes]
    return my_upvotes

def get_all_upvotes():
    return Upvote.query.all()

def get_all_upvotes_json():
    upvotes = Upvote.query.all()
    if not upvotes:
        return []
    upvotes = [upvote.get_json() for upvote in upvotes]
    return upvotes
