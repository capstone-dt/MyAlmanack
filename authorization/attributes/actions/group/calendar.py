from ..bounded_actions import UserToGroupAction
from authorization import policies


class ViewGroupCalendar(UserToGroupAction):
    policies = [
        # A user who is a group member can view a group's calendar.
        policies.user.group.UserIsGroupMember
    ]


class EditGroupCalendar(UserToGroupAction):
    policies = [
        # A user who is a group administrator can edit a group's calendar.
        policies.user.group.UserIsGroupAdministrator
    ]