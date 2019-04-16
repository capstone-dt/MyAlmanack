from authorization.decision import Policy


class UsersAreContacts(Policy):
    @classmethod
    def evaluate(cls, request):
        return (
            request.subject in request.resource.get_contacts()
            and # Just to make sure...
            request.resource in request.subject.get_contacts()
        )


class UsersShareCommonGroup(Policy):
    @classmethod
    def evaluate(cls, request):
        return len(
            request.subject.get_groups() & request.resource.get_groups()
        ) > 0