from authorization.decision import Policy


# This checks whether a user subject is a member of an event resource.
class UserIsEventMember(Policy):
    @classmethod
    def evaluate(cls, request):
        return request.subject in request.resource.members


# This checks whether a user resource is a member of an event context.
class UserResourceIsEventContextMember(Policy):
    @classmethod
    def evaluate(cls, request):
        return request.resource in request.context.members


# This checks whether a user subject is the creator of an event resource.
class UserIsEventCreator(Policy):
    @classmethod
    def evaluate(cls, request):
        return request.subject == request.resource.creator


# This checks whether a user subject is an administrator of an event resource.
class UserIsEventAdministrator(Policy):
    @classmethod
    def evaluate(cls, request):
        return request.subject in request.resource.administrators


# This checks whether a user subject is a participant of an event resource.
class UserIsEventParticipant(Policy):
    @classmethod
    def evaluate(cls, request):
        return request.subject in request.resource.participants