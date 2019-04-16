from ..bounded_actions import (
    BinaryUserAction, BinaryUserInviteAction, UserGroupAction, UserEventAction
)
from authorization import policies


"""
User invites
"""


class SendUserInvite(BinaryUserAction):
    policies = [
        # A user cannot send an invite to himself or herself.
        ~policies.miscellaneous.SubjectIsResource
        
        # A user cannot send an invite to someone who's already their contact.
        & ~policies.user.user.UsersAreContacts
    ]


class RevokeUserInvite(BinaryUserInviteAction):
    policies = [
        # A user can revoke an invite he or she had previously sent.
        policies.user.invite.UserSentInvite
    ]


class AcceptUserInvite(BinaryUserInviteAction):
    policies = [
        # A user can accept an invite sent to him or her.
        policies.user.invite.UserReceivedInvite
    ]


class RejectUserInvite(BinaryUserInviteAction):
    policies = [
        # A user can reject an invite sent to him or her.
        policies.user.invite.UserReceivedInvite
    ]


"""
Group invites
"""


class SendGroupInvite(BinaryUserAction):
    policies = [
        # A user cannot send an invite to himself or herself.
        ~policies.miscellaneous.SubjectIsResource
        
        # A user cannot send an invite to someone who's already in the group.
        # & ~policies.user.group.UserIsInGroup
        # TODO: subject = user1, resource = user2, context = group
    ]


class RevokeGroupInvite(UserGroupAction):
    policies = [
        # A user can revoke an invite he or she had previously sent.
        policies.user.invite.UserSentInvite
    ]


class AcceptGroupInvite(UserGroupAction):
    policies = [
        # A user can accept an invite sent to him or her.
        policies.user.invite.UserReceivedInvite
    ]


class RejectGroupInvite(UserGroupAction):
    policies = [
        # A user can reject an invite sent to him or her.
        policies.user.invite.UserReceivedInvite
    ]


"""
Event invites
"""


class SendEventInvite(BinaryUserAction):
    policies = [
        # A user cannot send an invite to himself or herself.
        ~policies.miscellaneous.SubjectIsResource
        
        # TODO: Same as group invite
        # &
    ]


class RevokeEventInvite(UserEventAction):
    policies = [
        # A user can revoke an invite he or she had previously sent.
        policies.user.invite.UserSentInvite
    ]


class AcceptEventInvite(UserEventAction):
    policies = [
        # A user can accept an invite sent to him or her.
        policies.user.invite.UserReceivedInvite
    ]


class RejectEventInvite(UserEventAction):
    policies = [
        # A user can reject an invite sent to him or her.
        policies.user.invite.UserReceivedInvite
    ]