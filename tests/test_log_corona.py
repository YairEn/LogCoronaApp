from LogCorona.models import Peoples
from LogCorona.log_corona import delete_people_by_id, add_to_peoples, is_username_exist, get_username_data_by_id, \
    add_to_locations, get_location_id_by_name, get_peoples_by_user_id, add_to_log, delete_log


class TestAddPeople:
    @staticmethod
    def test_add_to_peoples(user):
        data = {
            'user_id': user,
            'first_name': 'yosi',
            'last_name': 'moshe',
        }
        people_id = add_to_peoples(**data)
        people = Peoples.select().where(Peoples.people_id == people_id)
        assert people == data
        delete_people_by_id(people_id)


class TestIsUserNameExist:
    @staticmethod
    def test_is_username_exist(user):
        username = 'yair1'
        assert is_username_exist(username) is True

    @staticmethod
    def test_is_username_dose_not_exist(user):
        username = 'yair123'
        assert is_username_exist(username) is False


class TestGetUsernameById:
    @staticmethod
    def test_get_username_data_by_id(user):
        username = get_username_data_by_id(user).username
        assert username == 'yair1'

    @staticmethod
    def test_get_username_data_by_id_invalid_useranme(user):
        username = get_username_data_by_id('moshe')
        assert username is None


class TestAddLocation:
    @staticmethod
    def test_add_to_locations(delete_tel_aviv_location):
        location_name = 'tel aviv'
        loc_id = add_to_locations(location_name)
        assert get_location_id_by_name(location_name) == loc_id


class TestGetPeopleByUserID:
    @staticmethod
    def test_get_peoples_by_user_id(user):
        data = {
            'user_id': user,
            'first_name': 'yosi',
            'last_name': 'moshe',
        }
        add_to_peoples(**data)
        peoples = get_peoples_by_user_id(user)
        assert data['first_name'] == peoples[0]['first_name']


class DeleteLog:
    @staticmethod
    def delete_log(user_yair_log):
        add_to_log('1', user_yair_log, '1', 'hey')
        delete_log(user_yair_log)
