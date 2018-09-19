from app import db, login_manager
from flask_login import UserMixin


@login_manager.user_loader
def load_user(user_id):
    return User.query.get(int(user_id))


class User(db.Model, UserMixin):
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(20), unique=True, nullable=False)
    email = db.Column(db.String(120), unique=True, nullable=False)
    image_file = db.Column(db.String(20), nullable=False, default='default.jpg')
    password = db.Column(db.String(60), nullable=False)

    def __repr__(self):
        return f"User('{self.username}', '{self.email}', '{self.image_file}')"


class Enroll(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'), nullable=False)
    class_number = db.Column(db.Integer, nullable=False)

    def __repr__(self):
        return f"Enroll('{self.user_id}', '{self.class_number}')"


class UWFaculty(db.Model):
    faculty_code = db.Column(db.String(10), primary_key=True)
    faculty_name = db.Column(db.String(20), nullable=False)

    def __repr__(self):
        return f"UWFaculty('{self.faculty_code}', '{self.faculty_name}')"

