from authorization.decision import Policy


class UserIsBlacklisted(Policy):
    @classmethod
    def evaluate(cls, request):
        from random import random
        return random() <= 0.5