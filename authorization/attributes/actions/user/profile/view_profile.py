from authorization.attributes import Action
from authorization import policies


class ViewProfile(Action):
    policies = [
        # User must not be blacklisted.
        ~policies.user.relationship.UserIsBlacklisted,
        
        # Users must be contacts.
        policies.user.relationship.UsersAreContacts
    ]