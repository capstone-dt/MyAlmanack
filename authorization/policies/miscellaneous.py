from ..decision.policy import Policy


# This always evaluates to true.
class Tautology(Policy):
    @classmethod
    def evaluate(cls, request):
        return True


# This checks whether the subject is the resource.
class SubjectIsResource(Policy):
    @classmethod
    def evaluate(cls, request):
        return request.subject == request.resource