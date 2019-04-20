from authorization.decision import Policy


# This checks whether two users are contacts.
class UsersAreContacts(Policy):
    @classmethod
    def evaluate(cls, request):
        return (
            request.subject in request.resource.contacts
            and # Just to make sure...
            request.resource in request.subject.contacts
        )


# This checks whether two users share a common group together.
class UsersShareCommonGroup(Policy):
    @classmethod
    def evaluate(cls, request):
        return len(request.subject.groups & request.resource.groups) > 0