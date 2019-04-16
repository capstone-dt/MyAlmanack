from ..bounded_actions import BinaryUserAction
from authorization import policies


class ViewUserCalendar(BinaryUserAction):
    policies = [
        # A user can view his or her own calendar.
        policies.miscellaneous.SubjectIsResource,
        
        # Users who are contacts can view each other's calendar.
        policies.user._user.UsersAreContacts
    ]


class EditUserCalendar(BinaryUserAction):
    policies = [
        # A user can edit his or her own calendar.
        policies.miscellaneous.SubjectIsResource
    ]