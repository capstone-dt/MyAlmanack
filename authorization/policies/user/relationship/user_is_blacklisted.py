from authorization.decision import Policy

# Python
from random import random


class UserIsBlacklisted(Policy):
    @classmethod
    def evaluate(cls, request):
        return random() <= 0.5