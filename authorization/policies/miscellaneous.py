from authorization.decision import Policy


class Tautology(Policy):
    @classmethod
    def evaluate(cls, request):
        return True


class SubjectIsResource(Policy):
    @classmethod
    def evaluate(cls, request):
        return request.subject == request.resource