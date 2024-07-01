import allure
from http import HTTPStatus
from helpers.data import Answers, INGREDIENTS, WRONG_INGREDIENTS, NONE_INGREDIENTS, Endpoints
from helpers.http_client import HttpMethods

class TestCreateOrders:

    @allure.title('Тест создания заказа')
    def test_create_order_user(self, http_client, token):
        with allure.step('Создание заказа пользователем'):
            response = http_client.send_request(HttpMethods.POST, Endpoints.ORDER, headers=token, data=INGREDIENTS)
            assert response.status_code == HTTPStatus.OK
            assert response.json()['order']['number'] != None and response.json()['success'] == True

    @allure.title('Тест создания заказа без авторизации')
    def test_create_order_unauthorized_user(self, http_client):
        with allure.step('Создание заказа неавторизованным пользователем'):
            response = http_client.send_request(HttpMethods.POST,  Endpoints.ORDER, data=INGREDIENTS)
            assert response.status_code == HTTPStatus.OK
            assert response.json()['order']['number'] != None and response.json()['success'] == True

    @allure.title('Тест создания заказа без заполнения ингредиентов')
    def test_create_order_without_ingredients(self, http_client, token):
        with allure.step('Создание заказа пользователем без заполнения ингредиентов'):
            response = http_client.send_request(HttpMethods.POST,  Endpoints.ORDER, headers=token, data=NONE_INGREDIENTS)
            assert response.status_code == HTTPStatus.BAD_REQUEST
            assert response.json()['message'] == Answers.WITHOUT_INGREDIENTS and response.json()['success'] == False

    @allure.title('Тест создания заказа с некорректным хэшем ингредиентов')
    def test_create_order_with_incorrect_id_ingredient(self, http_client, token):
        with (allure.step('Создание заказа пользователем с некорректным хэшем ингредиентов')):
            payload = WRONG_INGREDIENTS
            response = http_client.send_request(HttpMethods.POST,  Endpoints.ORDER, headers=token, data=payload)
            assert response.status_code == HTTPStatus.INTERNAL_SERVER_ERROR

class TestGetOrders:


    @allure.title('Тест получения заказа пользователя')
    def test_get_order_user(self, http_client, token):
        with allure.step('Получение информации заказов пользователя'):
            response = http_client.send_request(HttpMethods.GET, Endpoints.ORDER, headers=token)
            assert response.status_code == HTTPStatus.OK
            assert response.json()['success'] == True


    @allure.title('Тест получения заказа без авторизации')
    def test_get_order_without_authorization(self, http_client):
        with allure.step('Получение информации по заказам без авторизации'):
            response = http_client.send_request(HttpMethods.GET, Endpoints.ORDER, data=None)
            assert response.status_code == HTTPStatus.UNAUTHORIZED
            assert response.json()['message'] == Answers.NOT_AUTHORISED and response.json()['success'] == False