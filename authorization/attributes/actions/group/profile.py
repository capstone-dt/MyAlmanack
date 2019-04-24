from ..bounded_actions import UserToGroupAction
from authorization import policies


class ViewGroupProfile(UserToGroupAction):
    policies = [
        # Anyone can view a group's profile.
        policies.miscellaneous.Tautology
    ]


class EditGroupProfile(UserToGroupAction):
    policies = [
        # A group administrator can edit a group's profile.
        policies.user.group.UserIsGroupAdministrator
    ]