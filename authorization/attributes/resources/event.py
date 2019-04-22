from ..resource import Resource
from authorization.information.models import Event as WrappedEvent


class Event(Resource, WrappedEvent):
    pass