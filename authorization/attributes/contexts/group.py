from ..context import Context
from authorization.information.models import Group as WrappedGroup


class GroupContext(Context, WrappedGroup):
    pass