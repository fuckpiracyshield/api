import pytest
import os
import requests

from base import internal_authentication, post_request, authenticated_get_request

class TestAuthentication:

    access_token = None

    refresh_token = None

    @pytest.fixture(scope = "function", autouse = True)
    def setup_method(self, internal_authentication):
        self.access_token, self.refresh_token = internal_authentication

    def test_token_refresh(self):
        """
        Test authentication refresh token.
        """

        response = post_request('/api/v1/authentication/refresh', {
            'refresh_token': self.refresh_token
        })

        response_json = response.json()

        self.access_token = response_json['data']['access_token']

        assert response.status_code == 200

    def test_logout(self):
        """
        Test authentication logout.
        """

        response = authenticated_get_request('/api/v1/authentication/logout', self.access_token)

        assert response.status_code == 200
