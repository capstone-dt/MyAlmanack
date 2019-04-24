from ..bounded_actions import UserToGroupAction
from authorization import policies


class ViewGroup(UserToGroupAction):
    policies = [
        # Anyone can view a group.
        policies.miscellaneous.Tautology
    ]


class EditGroup(UserToGroupAction):
    policies = [
        # A group administrator can edit a group.
        policies.user.group.UserIsGroupAdministrator
    ]


class DeleteGroup(UserToGroupAction):
    policies = [
        # Nobody can delete a group (for now).
        ~policies.miscellaneous.Tautology
    ]