HTTP_OK = 200
HTTP_FOUND = 302
HTTP_404 = 404


class TestStat:
    VALID_NAME_IN_STAT_LIST = b'israel'
    THERE_IS_NO_DATA = b"You don't have log yet"

    @staticmethod
    def test_stat_return_redirect(client):
        assert client.get('/stat').status_code == HTTP_FOUND

    @staticmethod
    def test_stat_return_404(client):
        assert client.get('/statasdasd').status_code == HTTP_404

    @staticmethod
    def test_stat_return_data_ok(client, user_yai):
        data = {
            'loginUsername': 'yai',
            'loginPassword': 'en'
        }
        client.post('/login', data=data)
        assert client.get('/stat').status_code == HTTP_OK

    @staticmethod
    def test_stat_return_data(client):
        data = {
            'loginUsername': 'yai',
            'loginPassword': 'en'
        }
        client.post('/login', data=data)
        assert TestStat.THERE_IS_NO_DATA not in client.get('/stat').data

    @staticmethod
    def test_stat_return_empty_data(client, user):
        data = {
            'loginUsername': 'yair1',
            'loginPassword': 'en'
        }
        client.post('/login', data=data)
        assert TestStat.THERE_IS_NO_DATA in client.get('/stat').data
