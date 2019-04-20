from ..context import Context
from authorization.information.models import Event as WrappedEvent


class EventContext(Context, WrappedEvent):
    pass