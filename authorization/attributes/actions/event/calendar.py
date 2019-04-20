from ..bounded_actions import UserToEventAction
from authorization import policies


class ViewEventCalendar(UserToEventAction):
    policies = [
        # A user who is in a group can view the group's profile.
        policies.user.group.UserIsGroupMember
    ]


class EditEventCalendar(UserToEventAction):
    policies = [
        # A user can edit his or her own calendar.
        policies.miscellaneous.SubjectIsResource
    ]