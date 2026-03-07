from App.database import db
from sqlalchemy import ForeignKey

class Course(db.Model):
    __tablename__ = 'course'
    id = db.Column(db.Integer, primary_key=True)
    code = db.Column(db.String, nullable=False, unique=True)
    title =  db.Column(db.String, nullable=False)

    def __init__(self, code, title):
        self.code = code
        self.title = title

    def get_json(self):
        return {
            'id': self.id,
            'code': self.code,
            'title': self.title
        }
