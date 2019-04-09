from authorization.attributes.actions.user import BinaryUserAction
from authorization import policies


class ViewProfile(BinaryUserAction):
    policies = [
        # Users must be contacts.
        policies.user.relationship.UsersAreContacts
    ]