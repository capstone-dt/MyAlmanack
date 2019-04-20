from authorization.decision import Policy


# This checks whether a user subject is a member of a group resource.
class UserIsGroupMember(Policy):
    @classmethod
    def evaluate(cls, request):
        return request.subject in request.resource.members


# This checks whether a user resource is a member of a group context.
class UserResourceIsGroupContextMember(Policy):
    @classmethod
    def evaluate(cls, request):
        return request.resource in request.context.members


# This checks whether a user subject is an administrator of a group resource.
class UserIsGroupAdministrator(Policy):
    @classmethod
    def evaluate(cls, request):
        return request.subject in request.resource.administrators