from piracyshield_component.config import Config

import pytest
import os
import requests

application_config = Config('application').get('general')
api_config = Config('application').get('api')

URL = f"{application_config.get('domain')}:{api_config.get('port')}"

def get_request(endpoint: str):
    return requests.get(f'{URL}{endpoint}')

def post_request(endpoint: str, data: dict):
    return requests.post(f'{URL}{endpoint}', json = data)

def authenticated_get_request(endpoint: str, access_token: str):
    return requests.get(f'{URL}{endpoint}', headers = {
        'Authorization': f'Bearer {access_token}'
    })

def authenticated_post_request(endpoint: str, access_token: str, data: dict):
    return requests.post(f'{URL}{endpoint}', headers = {
        'Authorization': f'Bearer {access_token}'
    }, json = data)

def authenticate(email, password):
    """
    General authentication utility.
    """

    response = requests.post(f'{URL}/api/v1/authentication/login', json = {
        'email': email,
        'password': password
    })

    response_json = response.json()

    access_token = response_json['data']['access_token']
    refresh_token = response_json['data']['refresh_token']

    assert access_token is not None
    assert refresh_token is not None

    return [ access_token, refresh_token ]

@pytest.fixture
def internal_authentication():
    """
    Passes parameters to authenticate a provider account.
    """

    return authenticate(
        email = os.environ.get('PIRACYSHIELD_MOCK_INTERNAL_EMAIL'),
        password = os.environ.get('PIRACYSHIELD_MOCK_INTERNAL_PASSWORD')
    )

@pytest.fixture
def reporter_authentication():
    """
    Passes parameters to authenticate a provider account.
    """

    return authenticate(
        email = os.environ.get('PIRACYSHIELD_MOCK_REPORTER_EMAIL'),
        password = os.environ.get('PIRACYSHIELD_MOCK_REPORTER_PASSWORD')
    )

@pytest.fixture
def provider_authentication():
    """
    Passes parameters to authenticate a provider account.
    """

    return authenticate(
        email = os.environ.get('PIRACYSHIELD_MOCK_PROVIDER_EMAIL'),
        password = os.environ.get('PIRACYSHIELD_MOCK_PROVIDER_PASSWORD')
    )
