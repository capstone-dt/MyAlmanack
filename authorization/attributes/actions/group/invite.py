from ..bounded_actions import UserToGroupAction
from authorization import policies


class SendGroupInvite(UserToGroupAction):
    policies = [
        # A user can accept his or her own invite.
        policies.miscellaneous.SubjectIsResource
    ]


class RevokeGroupInvite(UserToGroupAction):
    policies = [
        # A user can accept his or her own invite.
        policies.miscellaneous.SubjectIsResource
    ]


class AcceptGroupInvite(UserToGroupAction):
    policies = [
        # A user can accept his or her own invite.
        policies.miscellaneous.SubjectIsResource
    ]


class RejectGroupInvite(UserToGroupAction):
    policies = [
        # A user can reject his or her own invite.
        policies.miscellaneous.SubjectIsResource
    ]