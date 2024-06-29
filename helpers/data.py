from faker import Faker

USER_CREDS = {
    'email': 'user.testovich@gmail.com',
    'name': 'testovich',
    'password': 'Password2'
    }
INGREDIENTS = {"ingredients": ['61c0c5a71d1f82001bdaaa6d', '61c0c5a71d1f82001bdaaa6f', '61c0c5a71d1f82001bdaaa72']}
NONE_INGREDIENTS = {"ingredients": None}
WRONG_INGREDIENTS = {"ingredients": ["61c0c5a71d1f82001bda212a6d"]}
WRONG_USER_DATA = [('test1', 'test1'), ('test2', 'test1')]
USER_DATA_WITHOUT_REQUIRED_FIELD = [('email', ''), ('name', ''), ('password', '')]
PATCH_USER_DATA = [('', 'testovich1', ''), ('', '', 'Password2'), ('user.testovich1@gmail.com', '', ''), ('user.testovich@gmail.com', 'testovich', 'Password1')]

class Generator:
    def generate_user_data(self):
        data = Faker()
        user_data = {
        "email": None,
        "name": None,
        "password": None
        }
        username = data.first_name()
        email = data.email()
        password = data.password()
        user_data["email"] = email
        user_data["name"] = username
        user_data["password"] = password
        return user_data


class Answers:

    DUPLICATE_USER = "User already exists"
    REQUIRED_FIELD = "Email, password and name are required fields"
    NOT_AUTHORISED = "You should be authorised"
    WRONG_DATA = "email or password are incorrect"
    WITHOUT_INGREDIENTS = "Ingredient ids must be provided"

class Endpoints:

    URL = 'https://stellarburgers.nomoreparties.site/api'
    CREATE_USER_POINT = '/auth/register'
    LOGIN_USER = '/auth/login'
    USER = '/auth/user'
    ORDER = '/orders'
