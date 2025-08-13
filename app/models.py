from datetime import date
from werkzeug.security import generate_password_hash, check_password_hash
from flask_login import UserMixin

from . import db, login_manager


class User(UserMixin, db.Model):
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(80), unique=True, nullable=False)
    email = db.Column(db.String(120), unique=True, nullable=False)
    password_hash = db.Column(db.String(128), nullable=False)

    def set_password(self, password: str) -> None:
        self.password_hash = generate_password_hash(password)

    def check_password(self, password: str) -> bool:
        return check_password_hash(self.password_hash, password)


class Reservation(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'), nullable=False)
    start_date = db.Column(db.Date, nullable=False)
    end_date = db.Column(db.Date, nullable=False)

    user = db.relationship('User', backref='reservations')

    def as_dict(self):
        return {
            'id': self.id,
            'title': self.user.username,
            'email': self.user.email,
            'start': self.start_date.isoformat(),
            'end': self.end_date.isoformat(),
        }


def is_available(start: date, end: date, exclude_id: int | None = None) -> bool:
    query = Reservation.query
    if exclude_id is not None:
        query = query.filter(Reservation.id != exclude_id)
    overlap = query.filter(Reservation.start_date <= end, Reservation.end_date >= start).first()
    return overlap is None


@login_manager.user_loader
def load_user(user_id):
    return User.query.get(int(user_id))
