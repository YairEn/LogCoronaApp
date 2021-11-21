HTTP_OK = 200
HTTP_404 = 404
HTTP_FOUND = 302


class TestRegister:
    ALREADY_IN_USE = b'The username is already in use, please choose other one'
    EMPTY_MSG = b'One or more of your inputs is empty Please fill the fields'

    @staticmethod
    def test_register_return_ok(client):
        assert client.get('/register').status_code == HTTP_OK

    @staticmethod
    def test_register_return_404(client):
        assert client.get('/register1').status_code == HTTP_404

    @staticmethod
    def test_register_one_or_more_fields_are_empty(client):
        data = {
            'registerFirstName': 'yai',
            'registerLastName': 'en',
            'registerUsername': '',
            'registerPassword': 'en'
        }
        assert TestRegister.EMPTY_MSG in client.post('/register', data=data).data

    @staticmethod
    def test_register_user_already_exist(client, user_yair):
        data = {
            'registerFirstName': 'yai',
            'registerLastName': 'en',
            'registerUsername': 'yair',
            'registerPassword': 'en'
        }
        assert TestRegister.ALREADY_IN_USE in client.post('/register', data=data).data

    @staticmethod
    def test_register_new_user(client, delete_user_yairengel):
        data = {
            'registerFirstName': 'yairengel',
            'registerLastName': 'en',
            'registerUsername': 'yairengel',
            'registerPassword': 'en'
        }
        assert client.post('/register', data=data).status_code == HTTP_FOUND


