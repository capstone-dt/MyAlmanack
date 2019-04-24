from ..resource import Resource
from authorization.information.models import User as WrappedUser


class User(Resource, WrappedUser):
    pass