import pytest
import requests

from base import URL

class TestErrors:

    def test_route_not_found(self):
        """
        Test a non existent route.
        """

        response = requests.get(f'{URL}/fake/route')

        assert response.status_code == 404

    def test_method_not_allowed(self):
        """
        Test an existing route with the wrong method.
        """

        response = requests.get(f'{URL}/api/v1/account/guest/create')

        assert response.status_code == 405

    def test_create_user(self):
        """
        Test a non authorized account creation request.
        """

        response = requests.post(f'{URL}/api/v1/account/guest/create', {'name': 'test'})

        assert response.status_code == 401

    def test_missing_authentication_parameter(self):
        """
        Miss a parameter.
        """

        response = requests.post(f'{URL}/api/v1/authentication/login', {'email': 'test@fake.com'})

        assert response.status_code == 400

    def test_fake_authentication(self):
        """
        Test using a non existent e-mail.
        """

        response = requests.post(f'{URL}/api/v1/authentication/login', {'email': 'test@fake.com', 'password': 'very_fake'})

        assert response.status_code == 400

    def test_bad_format_refresh_token(self):
        """
        Try to refresh a bad token.
        """

        response = requests.post(f'{URL}/api/v1/authentication/refresh', {'refresh_token': 'non valid token'})

        assert response.status_code == 400
