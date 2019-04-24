from ..resource import Resource
from authorization.information.models.invites import (
    UserInvite as WrappedUserInvite,
    GroupInvite as WrappedGroupInvite,
    EventInvite as WrappedEventInvite
)


class UserInvite(Resource, WrappedUserInvite):
    pass


class GroupInvite(Resource, WrappedGroupInvite):
    pass


class EventInvite(Resource, WrappedEventInvite):
    pass