from authorization.attributes import Action
from authorization.attributes.subjects import User as UserSubject
from authorization.attributes.resources import User as UserResource
from authorization.attributes.contexts import HttpRequestContext


class BinaryUserAction(Action):
    _subject_class = UserSubject
    _resource_class = UserResource


class BinaryUserHttpAction(BinaryUserAction):
    _context_class = HttpRequestContext