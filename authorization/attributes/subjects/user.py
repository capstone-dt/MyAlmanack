from ..subject import Subject
from authorization.information.models import User as WrappedUser


class User(Subject, WrappedUser):
    pass