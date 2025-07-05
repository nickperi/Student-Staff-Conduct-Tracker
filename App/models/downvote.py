from App.database import db
from sqlalchemy import ForeignKey

class Downvote(db.Model):
    __tablename__ = "downvote"
    id = db.Column(db.Integer, primary_key=True)
    staffid = db.Column(db.Integer, db.ForeignKey('staff.id'), nullable=False)
    reviewid = db.Column(db.Integer, db.ForeignKey('review.id'), nullable=False)

    def __init__(self, staffid, reviewid):
        self.staffid = staffid
        self.reviewid = reviewid

    def get_json(self):
        return {
            'id': self.id,
            'staff id': self.staffid,
            'review id': self.reviewid
        }
