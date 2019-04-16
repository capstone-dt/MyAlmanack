from authorization.attributes import Action
from authorization.attributes.subjects import (
    User as UserSubject,
    Group as GroupSubject
)
from authorization.attributes.resources import (
    User as UserResource,
    Group as GroupResource,
    UserInvite as UserInviteResource,
    GroupInvite as GroupInviteResource,
    EventInvite as EventInviteResource
)


class BinaryUserAction(Action):
    _subject_class = UserSubject
    _resource_class = UserResource


class BinaryGroupAction(Action):
    _subject_class = GroupSubject
    _resource_class = GroupResource


class UserGroupAction(Action):
    _subject_class = UserSubject
    _resource_class = GroupResource


class GroupUserAction(Action):
    _subject_class = GroupSubject
    _resource_class = UserResource


class BinaryUserInviteAction(Action):
    _subject_class = UserSubject
    _resource_class = UserInviteResource


class UserGroupInviteAction(Action):
    _subject_class = UserSubject
    _resource_class = GroupInviteResource


class UserEventInviteAction(Action):
    _subject_class = UserSubject
    _resource_class = EventInviteResource