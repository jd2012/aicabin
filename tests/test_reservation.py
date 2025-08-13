import os
import sys
import unittest
from datetime import date

sys.path.append(os.path.dirname(os.path.dirname(__file__)))

from app import create_app, db
from app.models import User, Reservation, is_available


class ReservationTestCase(unittest.TestCase):
    def setUp(self):
        self.app = create_app()
        self.app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///:memory:'
        self.app.config['TESTING'] = True
        with self.app.app_context():
            db.create_all()
            user = User(username='u', email='u@example.com')
            user.set_password('pass')
            db.session.add(user)
            db.session.commit()
            self.user_id = user.id

    def tearDown(self):
        with self.app.app_context():
            db.drop_all()

    def test_overlap(self):
        with self.app.app_context():
            r1 = Reservation(user_id=self.user_id, start_date=date(2023, 1, 10), end_date=date(2023, 1, 15))
            db.session.add(r1)
            db.session.commit()
            self.assertFalse(is_available(date(2023, 1, 14), date(2023, 1, 20)))
            self.assertTrue(is_available(date(2023, 1, 16), date(2023, 1, 20)))

    def test_exclude_id(self):
        with self.app.app_context():
            r1 = Reservation(user_id=self.user_id, start_date=date(2023, 2, 1), end_date=date(2023, 2, 5))
            db.session.add(r1)
            db.session.commit()
            self.assertTrue(is_available(date(2023, 2, 1), date(2023, 2, 5), exclude_id=r1.id))


if __name__ == '__main__':
    unittest.main()
