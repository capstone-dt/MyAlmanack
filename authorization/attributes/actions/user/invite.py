from ..bounded_actions import BinaryUserAction
from authorization import policies


class SendUserInvite(BinaryUserAction):
    policies = [
        # A user cannot send an invite to someone who's already their contact.
        ~policies.user._user.UsersAreContacts
    ]


class RevokeUserInvite(BinaryUserAction):
    policies = [
        # A user can revoke an invite he or she had previously sent.
        # policies.miscellaneous.SubjectIsResource
    ]


class AcceptUserInvite(BinaryUserAction):
    policies = [
        # A user can accept an invite sent to him or her.
        # policies.miscellaneous.SubjectIsResource
    ]


class RejectUserInvite(BinaryUserAction):
    policies = [
        # A user can reject an invite sent to him or her.
        # policies.miscellaneous.SubjectIsResource
    ]