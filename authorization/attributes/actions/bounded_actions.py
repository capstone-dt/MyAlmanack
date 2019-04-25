from authorization.attributes import Action
from authorization.attributes.subjects import User as UserSubject
from authorization.attributes.resources import (
    User as UserResource,
    Group as GroupResource,
    Event as EventResource,
    GroupInvite as GroupInviteResource,
    EventInvite as EventInviteResource,
    UserRequest as UserRequestResource,
    GroupRequest as GroupRequestResource
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


class UserToGroupInviteAction(Action):
    _subject_class = UserSubject
    _resource_class = GroupInviteResource


class UserToEventInviteAction(Action):
    _subject_class = UserSubject
    _resource_class = EventInviteResource


class UserToUserRequestAction(Action):
    _subject_class = UserSubject
    _resource_class = UserRequestResource


class UserToGroupRequestAction(Action):
    _subject_class = UserSubject
    _resource_class = GroupRequestResource