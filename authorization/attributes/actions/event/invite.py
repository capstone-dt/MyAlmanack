from ..bounded_actions import UserToUserAction, UserToEventAction
from authorization.attributes.contexts import EventContext
from authorization import policies


class ViewEventInvite(UserToEventAction):
    policies = [
        # A user can view an invite he or she had previously sent.
        policies.user.invite.UserSentInvite,
        
        # A user can view an invite sent to him or her.
        policies.user.invite.UserReceivedInvite
    ]


class EditEventInvite(UserToEventAction):
    policies = [
        # A user can edit an invite he or she had previously sent.
        policies.user.invite.UserSentInvite
    ]


class SendEventInvite(UserToUserAction):
    # Special case: subject = user1, resource = user2, context = event
    _context_class = EventContext
    
    policies = [
        # A user cannot send an invite to himself or herself.
        ~policies.miscellaneous.SubjectIsResource
        
        # A user cannot send an invite to someone who's already in the event.
        & ~policies.user.event.UserResourceIsEventContextMember
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