from ..bounded_actions import BinaryUserAction
from authorization import policies


class SendUserInvite(BinaryUserAction):
    policies = [
        # A user cannot send an invite to someone who's already their contact.
        ~policies.user.relationship.UsersAreContacts
    ]


class RevokeUserInvite(BinaryUserAction):
    policies = [
        # A user can revoke a user invite he or she had previously sent.
        policies.miscellaneous.SubjectIsResource
    ]


class AcceptUserInvite(BinaryUserAction):
    policies = [
        # A user can accept his or her own invite.
        policies.miscellaneous.SubjectIsResource
    ]


class RejectUserInvite(BinaryUserAction):
    policies = [
        # A user can reject his or her own invite.
        policies.miscellaneous.SubjectIsResource
    ]