from ..bounded_actions import UserToUserAction
from authorization import policies


class ViewUserCalendar(UserToUserAction):
    policies = [
        # A user can view his or her own calendar.
        policies.miscellaneous.SubjectIsResource,
        
        # Users who are contacts can view each other's calendar.
        policies.user.user.UsersAreContacts
    ]


class EditUserCalendar(UserToUserAction):
    policies = [
        # A user can edit his or her own calendar.
        policies.miscellaneous.SubjectIsResource
    ]