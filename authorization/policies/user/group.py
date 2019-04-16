from authorization.decision import Policy


class UserIsGroupMember(Policy):
    @classmethod
    def evaluate(cls, request):
        return request.subject in request.resource.members


class UserIsGroupAdministrator(Policy):
    @classmethod
    def evaluate(cls, request):
        return request.subject in request.resource.administrators


# This checks whether the user subject is a member or administrator of a group.
class UserIsInGroup(Policy):
    @classmethod
    def evaluate(cls, request):
        return request.resource.contains_user(request.subject)


# This checks whether the user resource is a member or administrator of a group
#     context.
class UserResourceIsInGroupContext(Policy):
    @classmethod
    def evaluate(cls, request):
        return request.context.contains_user(request.resource)