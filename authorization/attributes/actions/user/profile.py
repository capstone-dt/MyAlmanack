from ..bounded_actions import BinaryUserAction
from authorization import policies


class ViewUserProfile(BinaryUserAction):
    policies = [
        # A user can view his or her own profile.
        policies.miscellaneous.SubjectIsResource,
        
        # Users who are contacts can view each other's profile.
        policies.user.relationship.UsersAreContacts,
        
        # Users who are in one or more groups together can view each other's
        #     profile.
        policies.user.relationship.UsersHaveACommonGroup
    ]


class EditUserProfile(BinaryUserAction):
    policies = [
        # A user can edit his or her own profile.
        policies.miscellaneous.SubjectIsResource
    ]