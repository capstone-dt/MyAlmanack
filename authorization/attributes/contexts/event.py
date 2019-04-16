from ..context import Context
from authorization.information import Event as WrappedEvent


class EventContext(Context, WrappedEvent):
    pass