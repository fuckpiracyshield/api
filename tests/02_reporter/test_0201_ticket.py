import pytest
import requests
import secrets

import sys
import os
import time

sys.path.append('../')

from base import reporter_authentication, authenticated_post_request

class TestReporterCreateTicket:

    ticket_wait_time = 76

    ticket_parameters = {
        'dda_id': '7b3d774097ca477687f29ad0968833ac',
        'description': '__MOCK_TICKET__',
        'forensic_evidence': {
            'hash': {}
        },
        'fqdn': [
            'mock-website.com',
            'mock-website-two.com'
        ],
        'ipv4': [
            '9.8.7.6',
            '1.1.1.1'
        ],
        'ipv6': [
            '2001:db8:3333:4444:5555:6666:7777:8888'
        ]
    }

    @pytest.fixture(scope = "function", autouse = True)
    def setup_method(self, reporter_authentication):
        self.access_token, self.refresh_token = reporter_authentication

    def test_create_and_remove_ticket(self):
        self.ticket_parameters['forensic_evidence']['hash'] = {
            'sha256': secrets.token_hex(32)
        }

        create_response = authenticated_post_request('/api/v1/ticket/create', self.access_token, self.ticket_parameters)

        assert create_response.status_code == 200
        assert create_response.json()['status'] == 'success'

        time.sleep(1)

        remove_response = authenticated_post_request('/api/v1/ticket/remove', self.access_token, {
            'ticket_id': create_response.json()['data']['ticket_id']
        })

        assert remove_response.status_code == 200
        assert remove_response.json()['status'] == 'success'

        time.sleep(1)

    def test_create_real_ticket(self):
        self.ticket_parameters['forensic_evidence']['hash'] = {
            'sha256': secrets.token_hex(32)
        }

        response = authenticated_post_request('/api/v1/ticket/create', self.access_token, self.ticket_parameters)

        assert response.status_code == 200
        assert response.json()['status'] == 'success'

        print(f"Waiting for the ticket to change status ({self.ticket_wait_time}s)")

        time.sleep(self.ticket_wait_time)
