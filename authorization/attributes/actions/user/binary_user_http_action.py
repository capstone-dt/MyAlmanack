from authorization.attributes import Action
from authorization.attributes.subjects import User as UserSubject
from authorization.attributes.resources import User as UserResource
from authorization.attributes.contexts import HttpRequestContext


class BinaryUserHttpAction(Action):
    _subject_class = UserSubject
    _resource_class = UserResource
    _context_class = HttpRequestContext