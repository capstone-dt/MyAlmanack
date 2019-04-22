from ..bounded_actions import UserToUserAction, UserToUserInviteAction
from authorization import policies


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