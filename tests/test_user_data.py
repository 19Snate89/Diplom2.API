import allure
import pytest
from helpers.data import Generator, Answers, USER_CREDS, USER_DATA_WITHOUT_REQUIRED_FIELD, PATCH_USER_DATA, WRONG_USER_DATA
from helpers.http_client import HttpMethods

CREATE_USER_POINT = '/auth/register'
LOGIN_USER = '/auth/login'
USER = '/auth/user'

class TestCreateUser():

    @allure.title('Тест создания пользователя')
    def test_create_uniq_user(self, http_client):
        with allure.step('Создаем пользователя в системе'):
            gen = Generator()
            payload = gen.generate_user_data()
            response = http_client.send_request(HttpMethods.POST, CREATE_USER_POINT, data=payload)
            assert response.status_code == 200
            assert response.json()['accessToken'] != None and response.json()['success'] == True

    @allure.title('Тест создания пользователя с повторными данными')
    def test_create_register_already_have_create(self, http_client):
        with allure.step('Создаем пользователя в системе с уже существующими значениями'):
            payload = USER_CREDS
            response = http_client.send_request(HttpMethods.POST, CREATE_USER_POINT, data=payload)
            assert response.status_code == 403
            assert response.json()['message'] == Answers.DUPLICATE_USER and response.json()['success'] == False

    @allure.title('Тест создания пользователя без заполненного обязательного поля')
    @pytest.mark.parametrize(('email', 'name', 'password'), USER_DATA_WITHOUT_REQUIRED_FIELD)
    def test_create_user_without_one_required_field(self, http_client, email, name, password):
        with allure.step('Создаем пользователя в системе'):
            payload = {
                'email': email,
                'name': name,
                'password': password
            }
            response = http_client.send_request(HttpMethods.POST, CREATE_USER_POINT, data=payload)
            assert response.status_code == 403
            assert response.json()['message'] == Answers.REQUIRED_FIELD and response.json()['success'] == False


class TestLoginUser:

    @allure.title('Тест авторизации под пользователем')
    def test_login_user(self, http_client):
        with allure.step('Авторизируемся пользователем в системе'):
            payload = {
                'email': USER_CREDS['email'],
                'password': USER_CREDS['password']
            }
            response = http_client.send_request(HttpMethods.POST, LOGIN_USER, data=payload)
            assert response.status_code == 200
            assert response.json()['accessToken'] != None and response.json()['success'] == True

    @allure.title('Тест авторизации под пользователем с некорректными данными')
    @pytest.mark.parametrize(('email', 'password'), WRONG_USER_DATA)
    def test_login_with_wrong_data(self, http_client, email, password):
        with allure.step('Обновление данных без авторизации'):
            payload = {
                'email': email,
                'password': password
            }
            response = http_client.send_request(HttpMethods.POST, LOGIN_USER, data=payload)
            assert response.status_code == 401
            assert response.json()['message'] == Answers.WRONG_DATA and response.json()['success'] == False

class TestChangeUserData:

    def test_create_uniq_use(self, http_client, authorization_user):
        with allure.step('Авторизируемся пользователем в системе'):
            request, email, name, password = authorization_user
            token = {"Authorization": f'{request.json()['accessToken']}'}
            new_email = 'newemail123@new.com'
            payload = {
                'email': new_email,
                'name': name,
                'password': password
            }
            response = http_client.send_request(HttpMethods.PATCH, USER, headers=token, data=payload)
            print(response.content)
            assert response.json()['success'] == True
            answer = http_client.send_request(HttpMethods.GET, USER, headers=token)
            print(answer.json()['user'])
            assert answer.json()['user']['email'] == new_email


    @allure.title('Тест изменения имени пользователя')
    def test_create_uniq_user(self, http_client, authorization_user):
        with allure.step('Авторизируемся пользователем в системе'):
            requests, email, name, password = authorization_user
            token = {"Authorization": f'{requests.json()['accessToken']}'}
            new_name = 'test'
            payload = {
                'email': email,
                'name': new_name,
                'password': password
            }
            response = http_client.send_request(HttpMethods.PATCH, USER, headers=token, data=payload)
            assert response.json()['success'] == True
            answer = http_client.send_request(HttpMethods.GET, USER, headers=token)
            print(answer.json()['user'])
            assert answer.json()['user']['name'] == new_name


    @allure.title('Тест изменения пароля пользователя')
    def test_create_uniq_user(self, http_client, authorization_user):
        with allure.step('Авторизируемся пользователем в системе'):
            requests, email, name, password = authorization_user
            token = {"Authorization": f'{requests.json()['accessToken']}'}
            print(token)
            new_password = 'Password2'
            payload = {
                'email': email,
                'name': name,
                'password': new_password
            }
            print(f'\n{payload}')
            response = http_client.send_request(HttpMethods.PATCH, USER, headers=token, data=payload)
            assert response.json()['success'] == True


    @allure.title('Тест изменения данных неавторизованного пользователя')
    @pytest.mark.parametrize(('email', 'name', 'password'), PATCH_USER_DATA)
    def test_create_register_already_have_create(self, http_client, email, name, password):
        with allure.step('Обновление данных без авторизации'):
            payload = {
                'email': email,
                'name': name,
                'password': password
            }
            response = http_client.send_request(HttpMethods.PATCH, USER, data=payload)
            assert response.status_code == 401
            assert response.json()['message'] == Answers.NOT_AUTHORISED and response.json()['success'] == False

