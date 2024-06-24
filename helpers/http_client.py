import requests
import allure
from logging import getLogger

logger = getLogger(__name__)


class HttpMethods(str):

    POST = "POST"
    GET = "GET"
    DELETE = "DELETE"
    PATCH = "PATCH"

class HttpClient:

    def __init__(self, url):
        self.base_url = url

    def send_request(self, method, endpoint, **kwargs):
        url = f"{self.base_url}{endpoint}"

        if kwargs:

            try:
                with allure.step(f"Отправлен запрос {method} on {url}"):
                    response = requests.request(method, url, **kwargs)
            except requests.RequestException as e:
                logger.error(f"Запрос {method} не может быть отправлен на {url}. Ошибка {e}")
            else:
                logger.info(
                    f'Запрос {method} направлен на {url} \n'
                    f'Данные запроса {response.request.body} \n'
                    f'Ответный статус код {response.status_code} \n'
                    f'Ответ{response.text} \n'
                    f'Ответ заголовка {response.headers} \n'
                )
                return response
