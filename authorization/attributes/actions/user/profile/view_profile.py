from authorization.attributes.actions.user import BinaryUserAction
from authorization import policies


class ViewProfile(BinaryUserAction):
    policies = [
        # A user can view his or her own profile.
        policies.miscellaneous.SubjectIsResource,
        
        # Users who are contacts can view each other's profile.
        policies.user.relationship.UsersAreContacts
    ]