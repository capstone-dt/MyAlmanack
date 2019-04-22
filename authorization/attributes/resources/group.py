from ..resource import Resource
from authorization.information.models import Group as WrappedGroup


class Group(Resource, WrappedGroup):
    pass