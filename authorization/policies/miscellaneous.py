from authorization.decision import Policy


class SubjectIsResource(Policy):
    @classmethod
    def evaluate(cls, request):
        return request.subject == request.resource