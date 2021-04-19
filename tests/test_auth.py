from flask import url_for

from axahlucky.models import User
from axahlucky.settings import Operations
from axahlucky.utils import generate_token
from tests.base import BaseTestCase


class AuthTestCase(BaseTestCase):

    def test_login_normal_user(self):
        response = self.login()
        data = response.get_data(as_text=True)
        self.assertIn('Welcome back.', data)