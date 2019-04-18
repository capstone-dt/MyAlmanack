from ..bounded_actions import (
    UserToUserAction, UserToGroupAction, UserToEventAction,
    UserToUserInviteAction
)
from authorization.attributes.contexts import GroupContext, EventContext
from authorization import policies


"""
User invites
"""


class SendUserInvite(UserToUserAction):
    policies = [
        # A user cannot send an invite to himself or herself.
        ~policies.miscellaneous.SubjectIsResource
        
        # A user cannot send an invite to someone who's already their contact.
        & ~policies.user.user.UsersAreContacts
    ]


class RevokeUserInvite(UserToUserInviteAction):
    policies = [
        # A user can revoke an invite he or she had previously sent.
        policies.user.invite.UserSentInvite
    ]


class AcceptUserInvite(UserToUserInviteAction):
    policies = [
        # A user can accept an invite sent to him or her.
        policies.user.invite.UserReceivedInvite
    ]


class RejectUserInvite(UserToUserInviteAction):
    policies = [
        # A user can reject an invite sent to him or her.
        policies.user.invite.UserReceivedInvite
    ]


"""
Group invites
"""


class SendGroupInvite(UserToUserAction):
    # Special case: subject = user1, resource = user2, context = group
    _context_class = GroupContext
    
    policies = [
        # A user cannot send an invite to himself or herself.
        ~policies.miscellaneous.SubjectIsResource
        
        # A user cannot send an invite to someone who's already in the group.
        & ~policies.user.group.UserResourceIsInGroupContext
    ]


class RevokeGroupInvite(UserToGroupAction):
    policies = [
        # A user can revoke an invite he or she had previously sent.
        policies.user.invite.UserSentInvite
    ]


class AcceptGroupInvite(UserToGroupAction):
    policies = [
        # A user can accept an invite sent to him or her.
        policies.user.invite.UserReceivedInvite
    ]


class RejectGroupInvite(UserToGroupAction):
    policies = [
        # A user can reject an invite sent to him or her.
        policies.user.invite.UserReceivedInvite
    ]


"""
Event invites
"""


class SendEventInvite(UserToUserAction):
    # Special case: subject = user1, resource = user2, context = event
    _context_class = EventContext
    
    policies = [
        # A user cannot send an invite to himself or herself.
        ~policies.miscellaneous.SubjectIsResource
        
        # A user cannot send an invite to someone who's already in the event.
        & ~policies.user.event.UserResourceIsInEventContext
    ]


class RevokeEventInvite(UserToEventAction):
    policies = [
        # A user can revoke an invite he or she had previously sent.
        policies.user.invite.UserSentInvite
    ]


class AcceptEventInvite(UserToEventAction):
    policies = [
        # A user can accept an invite sent to him or her.
        policies.user.invite.UserReceivedInvite
    ]


class RejectEventInvite(UserToEventAction):
    policies = [
        # A user can reject an invite sent to him or her.
        policies.user.invite.UserReceivedInvite
    ]