from ..resource import Resource
from authorization.information import User as WrappedUser


class User(Resource, WrappedUser):
    pass