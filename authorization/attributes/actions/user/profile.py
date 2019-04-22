from ..bounded_actions import UserToUserAction
from authorization import policies


class ViewUserProfile(UserToUserAction):
    policies = [
        # A user can view his or her own profile.
        policies.miscellaneous.SubjectIsResource,
        
        # Users who are contacts can view each other's profile.
        policies.user.user.UsersAreContacts,
        
        # Users who are in one or more groups together can view each other's
        #     profile.
        policies.user.user.UsersShareCommonGroup
    ]


class EditUserProfile(UserToUserAction):
    policies = [
        # A user can edit his or her own profile.
        policies.miscellaneous.SubjectIsResource
    ]


class DeleteUserProfile(UserToUserAction):
    policies = [
        # A user can delete his or her own profile.
        policies.miscellaneous.SubjectIsResource
    ]