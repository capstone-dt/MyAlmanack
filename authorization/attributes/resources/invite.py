from ..resource import Resource
from authorization.information.models.invites import (
    GroupInvite as WrappedGroupInvite,
    EventInvite as WrappedEventInvite
)


class GroupInvite(Resource, WrappedGroupInvite):
    pass


class EventInvite(Resource, WrappedEventInvite):
    pass