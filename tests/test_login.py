HTTP_OK = 200
HTTP_404 = 404


class TestLogin:
    BAD_LOGIN_MESSAGE = b'Username or password are incorrect'
    EMPTY_INPUTS = b'Username or password are empty'

    @staticmethod
    def test_login_return_ok(client):
        assert client.get('/login').status_code == HTTP_OK

    @staticmethod
    def test_login_return_404(client):
        assert client.get('/login2').status_code == HTTP_404

    @staticmethod
    def test_login_empty_inputs(client):
        data = {
            'loginUsername': '',
            'loginPassword': ''
        }
        assert TestLogin.EMPTY_INPUTS in client.post('/login', data=data).data

    @staticmethod
    def test_login_username_and_password_is_wrong(client):
        data = {
            'loginUsername': 'asd',
            'loginPassword': '123'
        }
        assert TestLogin.BAD_LOGIN_MESSAGE in client.post('/login', data=data).data

    @staticmethod
    def test_login_password_is_valid_user(client, user):
        data = {
            'loginUsername': 'yair1',
            'loginPassword': 'en'
        }
        assert TestLogin.BAD_LOGIN_MESSAGE not in client.post('/login', data=data).data
