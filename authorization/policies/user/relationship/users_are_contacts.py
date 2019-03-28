from authorization.decision import Policy


class UsersAreContacts(Policy):
    @classmethod
    def evaluate(cls, request):
        return True