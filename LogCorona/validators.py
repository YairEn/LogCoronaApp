def validate_inputs(*args: str) -> bool:
    """
    This func validate the input by call is_empty func
    :param args: List of inputs
    :return: True or False
    """
    for i in args:
        if _is_empty(i):
            return True


def _is_empty(value: str) -> bool:
    """
    Thid func check if the value is empty
    :param value: input value
    :return: True or False
    """
    if not value.strip():
        return True
    return False
