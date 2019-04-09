from authorization.attributes.actions.user import BinaryUserHttpAction
from authorization import policies


class ViewProfile(BinaryUserHttpAction):
    policies = [
        # Users must be contacts.
        policies.user.relationship.UsersAreContacts
    ]