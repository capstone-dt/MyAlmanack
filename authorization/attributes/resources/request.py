from ..resource import Resource
from authorization.information.models.requests import (
    UserRequest as WrappedUserRequest,
    GroupRequest as WrappedGroupRequest
)


class UserRequest(Resource, WrappedUserRequest):
    pass


class GroupRequest(Resource, WrappedGroupRequest):
    pass