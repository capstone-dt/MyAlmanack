from authorization.attributes import Action
from authorization.attributes.subjects import User as UserSubject
from authorization.attributes.resources import User as UserResource
from authorization.attributes.contexts import HttpRequestContext
from authorization import policies


class ViewProfile(Action):
    # Define the class constraints for the authorization request.
    _subject_class = UserSubject
    _resource_class = UserResource
    _context_class = HttpRequestContext
    
    # Define evaluable policies.
    policies = [
        # Users must be contacts.
        policies.user.relationship.UsersAreContacts
    ]