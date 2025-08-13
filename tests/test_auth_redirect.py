import os
import sys
import unittest

sys.path.append(os.path.dirname(os.path.dirname(__file__)))

from app import create_app, db


class AuthRedirectTestCase(unittest.TestCase):
    def setUp(self):
        self.app = create_app()
        self.app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///:memory:'
        self.app.config['TESTING'] = True
        self.client = self.app.test_client()
        with self.app.app_context():
            db.create_all()

    def tearDown(self):
        with self.app.app_context():
            db.drop_all()

    def test_login_required_redirect(self):
        response = self.client.get('/portal')
        self.assertEqual(response.status_code, 302)
        self.assertTrue(response.headers['Location'].endswith('/login?next=%2Fportal'))


if __name__ == '__main__':
    unittest.main()
