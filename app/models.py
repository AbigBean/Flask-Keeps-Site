from app import db
from flask_login import UserMixin


class User(UserMixin, db.Model):
    __tablename__ = 'users_table'  # Should matche your created database table name

    id = db.Column(db.Integer, primary_key=True)
    user = db.Column(db.String(64), unique=True, nullable=False)
    email = db.Column(db.String(120), unique=True, nullable=False)
    password = db.Column(db.String(500))
    notes = db.relationship('Notes', backref='user', lazy=True) # Creating a relationship

    def __repr__(self):
        return str(self.id) + ' - ' + str(self.user)

class Notes(db.Model):
    __tablename__ = 'notes'

    id = db.Column(db.Integer, primary_key=True)
    content = db.Column(db.Text, nullable=False)
    user_id = db.Column(db.Integer, db.ForeignKey('users_table.id'), nullable=False) # Refers to the relationship


