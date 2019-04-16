from ..bounded_actions import UserGroupAction
from authorization import policies


class ViewGroupProfile(UserGroupAction):
    policies = [
        # Anyone can view a group's profile.
        policies.miscellaneous.Tautology
    ]


class EditGroupProfile(UserGroupAction):
    policies = [
        # A group administrator can edit a group's profile.
        policies.user.group.UserIsGroupAdministrator
    ]