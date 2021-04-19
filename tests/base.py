import unittest

from flask import url_for

from axahlucky import create_app
from axahlucky.extensions import db
from axahlucky.models import User, Opinion, Keyword

class BaseTestCase(unittest.TestCase):

    def setUp(self):
        app = create_app('testing')
        self.context = app.test_request_context()
        self.context.push()
        self.client = app.test_client()
        self.runner = app.test_cli_runner()

        db.create_all()

        user1 = User(email="user1@axahlucky.com", username="user1", confirmed=True)
        user1.set_password('123456')

        keyword1 = Keyword(content="keyword1")
        keyword2 = Keyword(content="keyword2")
        opinion1 = Opinion(content="opinion1")
        opinion1.add_keyword(keyword1)
        opinion1.add_keyword(keyword2)

        db.session.add_all([user1, keyword1, keyword2, opinion1 ])
        db.session.commit()
        

    def tearDown(self):
        db.drop_all()
        self.context.pop()

    def login(self, username=None, password=None):
        if username is None and password is None:
            username = 'user1'
            password = '123456'
        return self.client.post(url_for('auth.login'), data=dict(
            username=username,
            password=password
        ), follow_redirects=True)

    def logout(self):
        return self.client.get(url_for('auth.logout'), follow_redirects=True)