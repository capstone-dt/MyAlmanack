from ..bounded_actions import UserToGroupAction, UserToGroupRequestAction
from authorization import policies


class ViewGroupRequest(UserToGroupRequestAction):
    policies = [
        # A user can view a group request he or she had previously sent.
        policies.user.request.UserSentRequest,
        
        # A user can view a group request sent to him or her.
        policies.user.request.UserReceivedRequest
    ]


class EditGroupRequest(UserToGroupRequestAction):
    policies = [
        # A user can edit a group request he or she had previously sent.
        policies.user.request.UserSentRequest
    ]


class SendGroupRequest(UserToGroupAction):
    policies = [
        # A user cannot send a group request to himself or herself.
        ~policies.miscellaneous.SubjectIsResource
        
        # A user cannot send a group request to a group if they are already in
        #     the group.
        & ~policies.user.group.UserIsGroupMember
        
        # A user cannot send a group request to a group that they have already
        #     sent a group request to.
        & ~policies.user.group.UserSentGroupRequest
    ]


class RevokeGroupRequest(UserToGroupRequestAction):
    policies = [
        # A user can revoke a group request he or she had previously sent.
        policies.user.request.UserSentRequest
    ]


class AcceptGroupRequest(UserToGroupRequestAction):
    policies = [
        # A user can accept a group request sent to him or her.
        policies.user.request.UserReceivedRequest
    ]


class RejectGroupRequest(UserToGroupRequestAction):
    policies = [
        # A user can reject a group request sent to him or her.
        policies.user.request.UserReceivedRequest
    ]