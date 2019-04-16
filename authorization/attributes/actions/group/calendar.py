from ..bounded_actions import UserGroupAction
from authorization import policies


class ViewGroupCalendar(UserGroupAction):
    policies = [
        # Users who are contacts can view each other's calendar.
        policies.user.relationship.UsersAreContacts
    ]


class EditGroupCalendar(UserGroupAction):
    policies = [
        # A user can edit his or her own calendar.
        policies.miscellaneous.SubjectIsResource
    ]