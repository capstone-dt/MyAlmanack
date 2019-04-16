from ..bounded_actions import UserGroupAction
from authorization import policies


class ViewGroupCalendar(UserGroupAction):
    policies = [
        # A user who is in a group can view the group's profile.
        policies.user.group.UserIsInGroup
    ]


class EditGroupCalendar(UserGroupAction):
    policies = [
        # A user can edit his or her own calendar.
        policies.miscellaneous.SubjectIsResource
    ]