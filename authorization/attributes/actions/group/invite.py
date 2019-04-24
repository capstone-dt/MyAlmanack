from ..bounded_actions import UserToUserAction, UserToGroupAction
from authorization.attributes.contexts import GroupContext
from authorization import policies


class ViewGroupInvite(UserToGroupAction):
    policies = [
        # A user can view an invite he or she had previously sent.
        policies.user.invite.UserSentInvite,
        
        # A user can view an invite sent to him or her.
        policies.user.invite.UserReceivedInvite
    ]


class EditGroupInvite(UserToGroupAction):
    policies = [
        # A user can edit an invite he or she had previously sent.
        policies.user.invite.UserSentInvite
    ]


class SendGroupInvite(UserToUserAction):
    # Special case: subject = user1, resource = user2, context = group
    _context_class = GroupContext
    
    policies = [
        # A user cannot send an invite to himself or herself.
        ~policies.miscellaneous.SubjectIsResource
        
        # A user cannot send an invite to someone who's already in the group.
        & ~policies.user.group.UserResourceIsGroupContextMember
    ]


class RevokeGroupInvite(UserToGroupAction):
    policies = [
        # A user can revoke an invite he or she had previously sent.
        policies.user.invite.UserSentInvite
    ]


class AcceptGroupInvite(UserToGroupAction):
    policies = [
        # A user can accept an invite sent to him or her.
        policies.user.invite.UserReceivedInvite
    ]


class RejectGroupInvite(UserToGroupAction):
    policies = [
        # A user can reject an invite sent to him or her.
        policies.user.invite.UserReceivedInvite
    ]