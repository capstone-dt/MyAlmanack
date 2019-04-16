from ..context import Context
from authorization.information import Group as WrappedGroup


class GroupContext(Context, WrappedGroup):
    pass