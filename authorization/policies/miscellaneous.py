from ..decision.policy import Policy


# This always evaluates to true.
class Tautology(Policy):
    @staticmethod
    def evaluate(request):
        return True


# This checks whether the subject is the resource.
class SubjectIsResource(Policy):
    @staticmethod
    def evaluate(request):
        return request.subject == request.resource