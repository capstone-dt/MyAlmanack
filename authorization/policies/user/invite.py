from authorization.decision import Policy


# This checks whether a user subject is the sender of an invite resource.
class UserSentInvite(Policy):
    @classmethod
    def evaluate(cls, request):
        return request.resource in request.subject.sent_invites


# This checks whether a user subject is a receiver of an invite resource.
class UserReceivedInvite(Policy):
    @classmethod
    def evaluate(cls, request):
        return request.resource in request.subject.received_invites