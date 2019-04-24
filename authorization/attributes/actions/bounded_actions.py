from authorization.attributes import Action
from authorization.attributes.subjects import (
    User as UserSubject,
    Group as GroupSubject
)
from authorization.attributes.resources import (
    User as UserResource,
    Group as GroupResource,
    Event as EventResource,
    UserInvite as UserInviteResource,
    GroupInvite as GroupInviteResource,
    EventInvite as EventInviteResource
)


"""
User-to-X actions
"""


class UserToUserAction(Action):
    _subject_class = UserSubject
    _resource_class = UserResource


class UserToGroupAction(Action):
    _subject_class = UserSubject
    _resource_class = GroupResource


class UserToEventAction(Action):
    _subject_class = UserSubject
    _resource_class = EventResource


class UserToUserInviteAction(Action):
    _subject_class = UserSubject
    _resource_class = UserInviteResource


class UserToGroupInviteAction(Action):
    _subject_class = UserSubject
    _resource_class = GroupInviteResource


class UserToEventInviteAction(Action):
    _subject_class = UserSubject
    _resource_class = EventInviteResource


"""
Group-to-X actions
"""


class GroupToUserAction(Action):
    _subject_class = GroupSubject
    _resource_class = UserResource


class GroupToGroupAction(Action):
    _subject_class = GroupSubject
    _resource_class = GroupResource


class GroupToEventAction(Action):
    _subject_class = GroupSubject
    _resource_class = EventResource


class GroupToUserInviteAction(Action):
    _subject_class = GroupSubject
    _resource_class = UserInviteResource


class GroupToGroupInviteAction(Action):
    _subject_class = GroupSubject
    _resource_class = GroupInviteResource


class GroupToEventInviteAction(Action):
    _subject_class = GroupSubject
    _resource_class = EventInviteResource