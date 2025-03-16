from App.models.downvote import Downvote
from App.database import db

def get_downvote(id):
    return Downvote.query.get(id)

def get_all_downvotes():
    return Downvote.query.all()

def get_all_downvotes_json():
    downvotes = Downvote.query.all()
    if not downvotes:
        return []
    downvotes = [downvote.get_json() for downvote in downvotes]
    return downvotes