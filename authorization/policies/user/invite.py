from authorization.decision import Policy


class UserSentInvite(Policy):
    @classmethod
    def evaluate(cls, request):
        return request.resource in request.subject.sent_invites


class UserReceivedInvite(Policy):
    @classmethod
    def evaluate(cls, request):
        return request.resource in request.subject.received_invites