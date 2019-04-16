from ..subject import Subject
from authorization.information import User as WrappedUser


class User(Subject, WrappedUser):
    pass