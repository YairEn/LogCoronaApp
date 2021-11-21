from datetime import datetime
import logging
from typing import Any, Dict, List, Optional

import uuid

from LogCorona.exceptions import UserAlreadyExist
from LogCorona.models import CoronaLog, Locations, Peoples, Users
from LogCorona.utlis import generate_password
import peewee
from playhouse.shortcuts import model_to_dict

app_logger = logging.getLogger('log_corona_logger')


def get_all_users() -> List[Dict[str, str]]:
    """
    This func get all users from db
    :return: List of users
    """
    rows = Users.select(Users.first_name, Users.last_name, Users.password)
    peoples_list = []
    for row in rows:
        peoples_list.append(model_to_dict(row))
    return peoples_list


def get_log_data_by_user_id_and_filter_param(user_id: str, filter_param: str = '1') -> List[Dict[str, str]]:
    """
    This func get the the data of the log of the user from the tables
    :param user_id: the user id
    :param filter_param: another filter to the where clause the can be dynamic
    :return:List of the data of the users
    """
    rows = (
        CoronaLog.select(CoronaLog.log_id, Peoples.people_id, Peoples.first_name, Peoples.last_name,
                         Locations.location_name,
                         CoronaLog.create_date, CoronaLog.comments).join(
            Peoples).switch(CoronaLog).join(
            Locations).where(
            CoronaLog.user_id == user_id, filter_param)).order_by(
        CoronaLog.create_date.desc())
    peoples_list = []
    for row in rows:
        corona_log_id = row.log_id
        people_id = row.people_id.people_id
        first_name = row.people_id.first_name
        last_name = row.people_id.last_name
        loc_name = row.location_id.location_name
        create_date = row.create_date
        comment = row.comments
        people_data = {'corona_log_id': corona_log_id, 'people_id': people_id, 'first_name': first_name,
                       'last_name': last_name,
                       'location_name': loc_name,
                       'create_date': create_date,
                       'comment': comment}
        peoples_list.append(people_data)
    return peoples_list


def get_peoples_by_user_id(user_id: str) -> List[str]:
    """
    This func gets the peoples data by user_id, all the people that connect to the given user id
    :param user_id: given user id
    :return: List of all the peoples data
    """
    rows = Peoples.select(Peoples.first_name, Peoples.last_name).where(Peoples.user_id == user_id)
    peoples_list = []
    for row in rows:
        peoples_list.append(model_to_dict(row))
    return peoples_list


def add_user(first_name: str, last_name: str, username: str, password: str) -> str:
    """
    This func add new user to the db
    :param first_name:
    :param last_name:
    :param username:
    :param password:
    :return: the new user_id
    """
    if not is_username_exist(username):
        user_id = str(uuid.uuid4())
        hashed_password = generate_password(password.encode('utf-8'))

        Users.insert(user_id=user_id, first_name=first_name, last_name=last_name, username=username,
                     password=hashed_password).execute()
        return user_id
    else:
        raise UserAlreadyExist


def get_username_data_by_username(username: str) -> Any:
    """
    This func get username data by the given username
    :param username:
    :return: Users object of the given user
    """
    try:
        user = Users.select(Users.user_id, Users.username, Users.password).where(Users.username == username).get()
        return user
    except peewee.DoesNotExist as err:
        app_logger.error(err)
        return


def get_username_data_by_id(user_id: str) -> Any:
    """
    This func get username data by id
    :param user_id:
    :return:Users object of the given user id
    """
    try:
        user = Users.select(Users.user_id, Users.username, Users.password).where(Users.user_id == user_id).get()
        return user
    except peewee.DoesNotExist as err:
        app_logger.error(err)
        return


def is_username_exist(username: str) -> bool:
    """
    This func check if the user exist in the users table
    :param username:
    :return: bool
    """
    user = get_username_data_by_username(username)
    if user is not None:
        return True
    return False


def add_peoples_data(user_id: str, first_name: str, last_name: str, location: str, comment: str) -> None:
    """
    This func manage the add data of the new log, to the locations, corona_log, and peoples tables
    :param user_id:
    :param first_name:
    :param last_name:
    :param location:
    :param comment:
    :return: None
    """
    people_id = add_to_peoples(user_id, first_name, last_name)
    loc_id = add_to_locations(location)
    add_to_log(user_id, people_id, loc_id, comment)


def add_to_log(user_id: str, people_id: str, loc_id: str, comment: str) -> None:
    """
    This func add new log to the corona_log table
    :param user_id:
    :param people_id:
    :param loc_id:
    :param comment:
    :return: None
    """
    log_id = str(uuid.uuid4())
    date = datetime.now()
    CoronaLog.insert(log_id=log_id, user_id=user_id, people_id=people_id, location_id=loc_id,
                     create_date=date.strftime("%Y-%m-%d"), comments=comment).execute()


def add_to_peoples(user_id: str, first_name: str, last_name: str) -> str:
    """
    This func add new people to the peoples tables
    :param user_id:
    :param first_name:
    :param last_name:
    :return: People_id the generated
    """
    people_id = str(uuid.uuid4())
    Peoples.insert(people_id=people_id, user_id=user_id, first_name=first_name, last_name=last_name).execute()
    return people_id


def get_location_id_by_name(loc_name: str) -> Any:
    """
    This func get the location_id by location_name from locations table
    :param loc_name: location_name
    :return: location_id
    """
    try:
        location_data = Locations.select(Locations.location_id).where(
            Locations.location_name == loc_name).get()
    except peewee.DoesNotExist as err:
        app_logger.error(err)
        return
    else:
        return location_data.location_id


def add_to_locations(location_name: str) -> Any:
    """
    This func add new location to locations table
    :param location_name:
    :return: location id
    """
    loc_id = get_location_id_by_name(location_name)
    if loc_id is None:
        loc_id = str(uuid.uuid4())
        Locations.insert(location_id=loc_id, location_name=location_name).execute()
    return loc_id


def get_people_id_by_log_id(log_id: str) -> Any:
    """
    This func get people_id by the the corona_log_id from the corona_log_table
    :param log_id:
    :return: people_id
    """
    try:
        people_id = CoronaLog.select(CoronaLog.people_id).where(CoronaLog.log_id == log_id).get()
    except peewee.DoesNotExist as err:
        app_logger.error(err)
        return
    else:
        return people_id.people_id


def get_location_id_by_log_id(log_id: str) -> Any:
    """
    This func get the location_id by he corona_log_id from the corona_log_table
    :param log_id:
    :return: location_id
    """
    try:
        location_id = CoronaLog.select(CoronaLog.location_id).where(CoronaLog.log_id == log_id).get()
    except peewee.DoesNotExist as err:
        app_logger.error(err)
        return
    else:
        return location_id.location_id


def delete_log(corona_log_id: str) -> Any:
    """
    This func delete log by delete from the corona_table and from the peoples table
    :param corona_log_id: log_id to be deleted
    :return:
    """
    try:
        people_id = get_people_id_by_log_id(corona_log_id)
        CoronaLog.delete().where(CoronaLog.log_id == corona_log_id).execute()
    except peewee.DoesNotExist as err:
        app_logger.error(err)
        return
    else:
        delete_people_by_id(people_id)


def delete_people_by_id(people_id: str) -> None:
    """
    Delete people from peoples table by people_id
    :param people_id:
    :return:
    """
    try:
        Peoples.delete().where(Peoples.people_id == people_id).execute()
    except peewee.DoesNotExist as err:
        app_logger.error(err)
        return


def update_people_data(people_id: str, first_name: str, last_name: str) -> None:
    """
    This func update people data in peoples table, update the first_name and last_name
    :param people_id:
    :param first_name:
    :param last_name:
    :return:
    """
    try:
        people = Peoples.select(Peoples.first_name, Peoples.last_name).where(Peoples.people_id == people_id).get()
    except peewee.DoesNotExist as err:
        app_logger.error(err)
        return
    else:
        if not (people.first_name == first_name and people.last_name == last_name):
            try:
                Peoples.update(first_name=first_name, last_name=last_name).where(
                    Peoples.people_id == people_id).execute()
            except peewee.DoesNotExist as err:
                app_logger.error(err)
                return


def update_log(log_id: str, log_data: Optional[Dict[str, str]]) -> None:
    """
    This func manage the update corona_log in corona_tables and peoples and locations
    :param log_id: corona_log_id to be update
    :param log_data: corona_log_data - the data to be updated
    :return:
    """
    people_id = get_people_id_by_log_id(log_id)
    update_people_data(people_id, log_data['first_name'], log_data['last_name'])
    loc_id_by_log = get_location_id_by_log_id(log_id)
    loc_id = add_to_locations(log_data['location_name'])
    if loc_id_by_log != loc_id:
        CoronaLog.update(location_id=loc_id, create_date=log_data['date'], comments=log_data['comment']).where(
            CoronaLog.log_id == log_id).execute()
