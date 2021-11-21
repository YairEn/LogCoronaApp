from typing import Dict, List, Tuple

import bcrypt

INDEX_ZERO_LOG_ID = 0
INDEX_ONE = 1
UNDERSCORE = '_'


def generate_password(password):
    salt = bcrypt.gensalt(prefix=b'2b', rounds=10)
    hashed_password = bcrypt.hashpw(password, salt)
    return hashed_password


def extract_field_name(html_element_name: str) -> str:
    """
    This func extract the name of the field from the html element
    :param html_element_name: name of html element the consist of log_id and field name (like first_name)
    :return: the name of field
    """
    return html_element_name[html_element_name.find(UNDERSCORE) + INDEX_ONE:]


def extract_log_id(html_element_name: str) -> str:
    """
    This func extract the log_id from the html element
    :param html_element_name: name of html element the consist of log_id and field name (like log_id)
    :return: the log_id
    """
    return html_element_name.split(UNDERSCORE)[INDEX_ZERO_LOG_ID]


def extract_peoples_data(data_from_request: Dict[str, str]) -> Tuple[Dict[str, Dict[str, str]], List[str]]:
    """
    This func extract the the people data to be updated ot deleted and arrange it in new Dict and List
    :param data_from_request: The data that given from the client
    :return: Dict with all the relevant data and List with the relevant logs_id to be updated or deleted
    """
    peoples_data = {}
    ids_to_work_on = []
    for html_element_name, value in data_from_request.items():
        log_id = extract_log_id(html_element_name)
        if peoples_data.get(log_id):
            peoples_data[log_id].update(
                {extract_field_name(html_element_name): value.strip()})
            if log_id not in ids_to_work_on:
                ids_to_work_on.append(log_id)
        else:
            peoples_data[html_element_name] = {html_element_name: value.strip()}
    return peoples_data, ids_to_work_on
