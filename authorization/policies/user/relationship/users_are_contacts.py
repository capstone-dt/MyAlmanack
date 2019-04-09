from authorization.decision import Policy


class UsersAreContacts(Policy):
    @classmethod
    def evaluate(cls, request):
        return (
            request.subject in request.resource.get_contacts()
            and
            request.resource in request.subject.get_contacts()
        )