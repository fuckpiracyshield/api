import pytest
import requests

from base import get_request

class TestGeneral:

    def test_ping(self):
        """
        Check the API availability.
        """

        response = get_request('/api/v1/ping')

        assert response.status_code == 200
