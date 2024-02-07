import pytest
import requests

import sys
import os

sys.path.append('../')

from base import provider_authentication, authenticated_get_request

class TestProviderRetrieveTicketItems:

    @pytest.fixture(scope = "function", autouse = True)
    def setup_method(self, provider_authentication):
        self.access_token, self.refresh_token = provider_authentication

    def test_fqdn_get_all(self):
        response = authenticated_get_request('/api/v1/fqdn/get/all', self.access_token)

        assert response.status_code == 200
        assert response.json()['status'] == 'success'

    def test_fqdn_get_all_txt(self):
        response = authenticated_get_request('/api/v1/fqdn/get/all/txt', self.access_token)

        assert response.status_code == 200
        assert response.headers.get('Content-Type', '').lower() == 'text/plain; charset=utf-8'

    def test_ipv4_get_all(self):
        response = authenticated_get_request('/api/v1/fqdn/get/all', self.access_token)

        assert response.status_code == 200
        assert response.json()['status'] == 'success'

    def test_ipv4_get_all_txt(self):
        response = authenticated_get_request('/api/v1/fqdn/get/all/txt', self.access_token)

        assert response.status_code == 200
        assert response.headers.get('Content-Type', '').lower() == 'text/plain; charset=utf-8'
