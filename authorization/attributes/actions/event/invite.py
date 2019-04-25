from ..bounded_actions import UserToUserAction, UserToEventInviteAction
from authorization.attributes.contexts import EventContext
from authorization import policies


class ViewEventInvite(UserToEventInviteAction):
    policies = [
        # A user can view an event invite he or she had previously sent.
        policies.user.invite.UserSentInvite,
        
        # A user can view an event invite sent to him or her.
        policies.user.invite.UserReceivedInvite
    ]


class EditEventInvite(UserToEventInviteAction):
    policies = [
        # A user can edit an event invite he or she had previously sent.
        policies.user.invite.UserSentInvite
    ]


class SendEventInvite(UserToUserAction):
    # Special case: subject = user1, resource = user2, context = event
    _context_class = EventContext
    
    policies = [
        # A user cannot send an event invite to himself or herself.
        ~policies.miscellaneous.SubjectIsResource
        
        # A user must be an event creator or administrator.
        & (
            policies.user.event.UserIsEventContextCreator
            | policies.user.event.UserIsEventContextAdministrator
        )
        
        # A user cannot send an event invite to someone who's already in the
        #     event.
        & ~policies.user.event.UserResourceIsEventContextMember
        
        # A user cannot send an event invite to someone who has already been
        #     invited to the event.
        & ~policies.user.event.UserResourceIsInvitedToEventContext
    ]


class RevokeEventInvite(UserToEventInviteAction):
    policies = [
        # A user can revoke an event invite he or she had previously sent.
        policies.user.invite.UserSentInvite
    ]


class AcceptEventInvite(UserToEventInviteAction):
    policies = [
        # A user can accept an event invite sent to him or her.
        policies.user.invite.UserReceivedInvite
    ]


class RejectEventInvite(UserToEventInviteAction):
    policies = [
        # A user can reject an event invite sent to him or her.
        policies.user.invite.UserReceivedInvite
    ]