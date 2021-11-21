HTTP_OK = 200
HTTP_404 = 404


class TestHome:
    WELCOME_GENERAL = b'Welcome to the Corona Log website'
    WELCOME_USER = b'Who you met today?'

    @staticmethod
    def test_home_return_ok(client):
        assert client.get('/').status_code == HTTP_OK

    @staticmethod
    def test_home_return_404(client):
        assert client.get('/1').status_code == HTTP_404

    @staticmethod
    def test_home_return_home_html(client):
        assert TestHome.WELCOME_GENERAL in client.get('/').data

    @staticmethod
    def test_home_return_home_html_logged_user(client, user_yai):
        data = {
            'loginUsername': 'yai',
            'loginPassword': 'en'
        }
        client.post('/login', data=data)
        assert TestHome.WELCOME_USER in client.get('/').data
