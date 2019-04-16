from authorization.attributes import Action
from authorization.attributes.subjects import User as UserSubject
from authorization.attributes.resources import User as UserResource, Group
from authorization.attributes.contexts import HttpRequestContext


class BinaryUserAction(Action):
    _subject_class = UserSubject
    _resource_class = UserResource


class BinaryUserHttpAction(BinaryUserAction):
    _context_class = HttpRequestContext


class UserGroupAction(Action):
    _subject_class = UserSubject
    _resource_class = Group


class UserGroupHttpAction(UserGroupAction):
    _context_class = HttpRequestContext


class GroupUserAction(Action):
    _subject_class = Group
    _resource_class = UserResource


class GroupUserHttpAction(GroupUserAction):
    _context_class = HttpRequestContext