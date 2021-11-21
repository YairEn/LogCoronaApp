HTTP_OK = 200
HTTP_404 = 404
HTTP_FOUND = 302


class TestLogCoronaMain:

    @staticmethod
    def test_log_corona_main_return_ok(client):
        assert client.get('/log_corona_main').status_code == HTTP_FOUND

    @staticmethod
    def test_log_corona_main_return_404(client):
        assert client.get('/log_corona_main1').status_code == HTTP_404

    @staticmethod
    def test_log_corona_main_return_add_log(client, user_yai):
        data = {
            'loginUsername': 'yai',
            'loginPassword': 'en'
        }
        client.post('/login', data=data)
        data = {
            'first_name': 'yair1',
            'last_name': 'en',
            'location': 'israel',
            'comment': 'asdasd'
        }
        assert client.post('/log_corona_main', data=data).data
