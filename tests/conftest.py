import pytest
from helpers.http_client import HttpClient, HttpMethods
from helpers.data import USER_CREDS, Generator

URL = 'https://stellarburgers.nomoreparties.site/api'

@pytest.fixture()
def http_client():
    return HttpClient(URL)

@pytest.fixture()
def token(http_client):
    payload = {
        'email': USER_CREDS['email'],
        'password': USER_CREDS['password']
    }
    response = http_client.send_request(HttpMethods.POST, "/auth/login", data=payload)
    token = {"Authorization": f'{response.json()['accessToken']}'}
    return token

@pytest.fixture()
def generator_user(http_client):
    gen = Generator()
    data = gen.generate_user_data()
    payload = {
        'email': data['email'],
        'name': data['name'],
        'password': data['password']
    }
    response = http_client.send_request(HttpMethods.POST, "/auth/register", data=payload)
    token = {"Authorization": f'{response.json()['accessToken']}'}
    yield response, data['email'], data['name'], data['password']
    delete = http_client.send_request(HttpMethods.DELETE, "/auth/user", headers=token)


@pytest.fixture()
def authorization_user(http_client, generator_user):
    request, email, name, password = generator_user
    payload = {
        'email': email,
        'password': password
    }
    response = http_client.send_request(HttpMethods.POST, "/auth/login", data=payload)
    token = {"Authorization": f'{response.json()['accessToken']}'}
    yield response, email, name, password
    delete = http_client.send_request(HttpMethods.DELETE, "/auth/user", headers=token)





