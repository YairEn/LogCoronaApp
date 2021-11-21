class UserAlreadyExist(Exception):
    def __init__(self) -> None:
        self.msg = "The username is already in use, please choose other one"
