from ..subject import Subject
from authorization.information import Group as WrappedGroup


class Group(Subject, WrappedGroup):
    pass