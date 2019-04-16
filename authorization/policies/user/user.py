from authorization.decision import Policy


class UsersAreContacts(Policy):
    @classmethod
    def evaluate(cls, request):
        return (
            request.subject in request.resource.contacts
            and # Just to make sure...
            request.resource in request.subject.contacts
        )


class UsersShareCommonGroup(Policy):
    @classmethod
    def evaluate(cls, request):
        return len(request.subject.groups & request.resource.groups) > 0