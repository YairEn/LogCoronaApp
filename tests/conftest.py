import os
import tempfile

from LogCorona import app, db
from LogCorona.log_corona import add_user
from LogCorona.models import Users, Locations, ALL_MODELS
import pytest


@pytest.fixture
def client():
    db_fd, app.config['DATABASE'] = tempfile.mkstemp()
    app.config['TESTING'] = True
    db.create_tables(ALL_MODELS)
    with app.test_client() as client:
        yield client

    os.close(db_fd)
    os.unlink(app.config['DATABASE'])


@pytest.fixture
def user():
    user = add_user(first_name='yai', last_name='en', username='yair1', password='en')
    yield user
    Users.delete().where(Users.username == 'yair1').execute()


@pytest.fixture
def user_yai():
    user = add_user(first_name='yai', last_name='en', username='yai', password='en')
    yield user
    Users.delete().where(Users.username == 'yai').execute()


@pytest.fixture
def user_yair():
    Users.delete().where(Users.username == 'yair').execute()
    user = add_user(first_name='yai', last_name='en', username='yair', password='en')
    yield user
    Users.delete().where(Users.username == 'yair').execute()


@pytest.fixture
def delete_user_yairengel():
    Users.delete().where(Users.username == 'yairengel').execute()
    yield user


@pytest.fixture
def delete_tel_aviv_location():
    loc = Locations.delete().where(Locations.location_name == 'tel aviv').execute()
    yield loc


@pytest.fixture
def user_yair_log():
    user = Users.insert('1', first_name='yai', last_name='en', username='yair', password='en').execute()
    yield user
    Users.delete().where(Users.username == 'yair').execute()
