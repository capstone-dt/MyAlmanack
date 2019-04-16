from ..bounded_actions import UserGroupAction
from authorization import policies


class ViewGroupProfile(UserGroupAction):
    policies = [
        # Users who are contacts can view each other's profile.
        policies.user.relationship.UsersAreContacts,
        
        # Users who are in one or more groups together can view each other's
        #     profile.
        policies.user.relationship.UsersHaveACommonGroup
    ]


class EditGroupProfile(UserGroupAction):
    policies = [
        # A user can edit his or her own profile.
        policies.miscellaneous.SubjectIsResource
    ]