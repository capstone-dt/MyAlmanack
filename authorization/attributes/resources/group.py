from ..resource import Resource
from authorization.information import Group as WrappedGroup


class Group(Resource, WrappedGroup):
    pass