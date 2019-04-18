from ..bounded_actions import UserToGroupAction
from authorization import policies


class ViewGroupCalendar(UserToGroupAction):
    policies = [
        # A user who is in a group can view the group's profile.
        policies.user.group.UserIsInGroup
    ]


class EditGroupCalendar(UserToGroupAction):
    policies = [
        # A user can edit his or her own calendar.
        policies.miscellaneous.SubjectIsResource
    ]