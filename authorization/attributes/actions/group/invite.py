from ..bounded_actions import UserGroupAction
from authorization import policies


class SendGroupInvite(UserGroupAction):
    policies = [
        # A user can accept his or her own invite.
        policies.miscellaneous.SubjectIsResource
    ]


class RevokeGroupInvite(UserGroupAction):
    policies = [
        # A user can accept his or her own invite.
        policies.miscellaneous.SubjectIsResource
    ]


class AcceptGroupInvite(UserGroupAction):
    policies = [
        # A user can accept his or her own invite.
        policies.miscellaneous.SubjectIsResource
    ]


class RejectGroupInvite(UserGroupAction):
    policies = [
        # A user can reject his or her own invite.
        policies.miscellaneous.SubjectIsResource
    ]