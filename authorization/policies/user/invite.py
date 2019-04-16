from authorization.decision import Policy


class UserSentInvite(Policy):
    @classmethod
    def evaluate(cls, request):
        return False