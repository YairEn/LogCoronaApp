HTTP_OK = 200
HTTP_404 = 404
HTTP_ERROR = 302


class TestLogOut:

    @staticmethod
    def test_logout_return_ok(client):
        assert client.get('/logout').status_code == HTTP_ERROR

    @staticmethod
    def test_logout_return_404(client):
        assert client.get('/logout1').status_code == HTTP_404
