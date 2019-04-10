from authorization.attributes.actions.user import BinaryUserAction
from authorization import policies


class ViewProfile(BinaryUserAction):
    policies = [
        # A user can view his or her own profile.
        policies.miscellaneous.SubjectIsResource,
        
        # Users must be contacts.
        policies.user.relationship.UsersAreContacts
    ]