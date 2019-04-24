from ..subject import Subject
from authorization.information.models import Group as WrappedGroup


class Group(Subject, WrappedGroup):
    pass