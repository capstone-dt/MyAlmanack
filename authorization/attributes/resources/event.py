from ..resource import Resource
from authorization.information import Event as WrappedEvent


class Event(Resource, WrappedEvent):
    pass