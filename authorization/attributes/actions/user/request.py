from ..bounded_actions import UserToUserAction, UserToUserRequestAction
from authorization import policies


class ViewUserRequest(UserToUserRequestAction):
    policies = [
        # A user can view a user request he or she had previously sent.
        policies.user.request.UserSentRequest,
        
        # A user can view a user request sent to him or her.
        policies.user.request.UserReceivedRequest
    ]


class EditUserRequest(UserToUserRequestAction):
    policies = [
        # A user can edit a user request he or she had previously sent.
        policies.user.request.UserSentRequest
    ]


class SendUserRequest(UserToUserAction):
    policies = [
        # A user cannot send a user request to himself or herself.
        ~policies.miscellaneous.SubjectIsResource
        
        # A user cannot send a user request to someone who's already their
        #     contact.
        & ~policies.user.user.UsersAreContacts
        
        # A user cannot send a user request to someone who they have already
        #     sent a user request to.
        & ~policies.user.user.UserSentUserRequest
    ]


class RevokeUserRequest(UserToUserRequestAction):
    policies = [
        # A user can revoke a user request he or she had previously sent.
        policies.user.request.UserSentRequest
    ]


class AcceptUserRequest(UserToUserRequestAction):
    policies = [
        # A user can accept a user request sent to him or her.
        policies.user.request.UserReceivedRequest
    ]


class RejectUserRequest(UserToUserRequestAction):
    policies = [
        # A user can reject a user request sent to him or her.
        policies.user.request.UserReceivedRequest
    ]