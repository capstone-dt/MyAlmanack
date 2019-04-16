from authorization.decision import Policy


class UserIsEventMember(Policy):
    @classmethod
    def evaluate(cls, request):
        return request.subject in request.resource.members


class UserIsEventAdministrator(Policy):
    @classmethod
    def evaluate(cls, request):
        return request.subject in request.resource.administrators


# This checks whether the user subject is a member or administrator of an event.
class UserIsInEvent(Policy):
    @classmethod
    def evaluate(cls, request):
        return request.resource.contains_user(request.subject)


# This checks whether the user resource is a member or administrator of an event
#     context.
class UserResourceIsInEventContext(Policy):
    @classmethod
    def evaluate(cls, request):
        return request.context.contains_user(request.resource)