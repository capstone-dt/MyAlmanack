from .binary_user_action import BinaryUserAction
from authorization import policies


class ViewUserCalendar(BinaryUserAction):
    policies = [
        # A user can view his or her own profile.
        policies.miscellaneous.SubjectIsResource,
        
        # Users who are contacts can view each other's profile.
        policies.user.relationship.UsersAreContacts
    ]


class EditUserCalendar(BinaryUserAction):
    policies = [
        # A user can edit his or her own profile.
        policies.miscellaneous.SubjectIsResource
    ]