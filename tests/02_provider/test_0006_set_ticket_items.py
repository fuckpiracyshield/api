import pytest
import requests

import sys
import os

sys.path.append('../')

from base import provider_authentication, authenticated_post_request

class TestProviderSetTicketItems:

    @pytest.fixture(scope = "function", autouse = True)
    def setup_method(self, provider_authentication):
        self.access_token, self.refresh_token = provider_authentication

    def test_set_processed_non_existent(self):
        response = authenticated_post_request('/api/v1/ticket/item/set/processed', self.access_token, {
            'value': '1.2.3.4'
        })

        assert response.status_code == 400
        assert response.json()['status'] == 'error'

    def test_set_processed_fqdn(self):
        response = authenticated_post_request('/api/v1/ticket/item/set/processed', self.access_token, {
            'value': 'mock-website.com'
        })

        assert response.status_code == 200
        assert response.json()['status'] == 'success'

    def test_set_processed_ipv4(self):
        response = authenticated_post_request('/api/v1/ticket/item/set/processed', self.access_token, {
            'value': '9.8.7.6'
        })

        assert response.status_code == 200
        assert response.json()['status'] == 'success'
