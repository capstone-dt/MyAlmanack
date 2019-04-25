from ..bounded_actions import UserToUserAction, UserToGroupInviteAction
from authorization.attributes.contexts import GroupContext
from authorization import policies


class ViewGroupInvite(UserToGroupInviteAction):
    policies = [
        # A user can view a group invite he or she had previously sent.
        policies.user.invite.UserSentInvite,
        
        # A user can view a group invite sent to him or her.
        policies.user.invite.UserReceivedInvite
    ]


class EditGroupInvite(UserToGroupInviteAction):
    policies = [
        # A user can edit a group invite he or she had previously sent.
        policies.user.invite.UserSentInvite
    ]


class SendGroupInvite(UserToUserAction):
    # Special case: subject = user1, resource = user2, context = group
    _context_class = GroupContext
    
    policies = [
        # A user cannot send a group invite to himself or herself.
        ~policies.miscellaneous.SubjectIsResource
        
        # A user must be a group administrator.
        & policies.user.group.UserIsGroupContextAdministrator
        
        # A user cannot send a group invite to someone who's already in the
        #     group.
        & ~policies.user.group.UserResourceIsGroupContextMember
        
        # A user cannot send a group invite to someone who has already been
        #     invited to the group.
        & ~policies.user.group.UserResourceIsInvitedToGroupContext
    ]


class RevokeGroupInvite(UserToGroupInviteAction):
    policies = [
        # A user can revoke a group invite he or she had previously sent.
        policies.user.invite.UserSentInvite
    ]


class AcceptGroupInvite(UserToGroupInviteAction):
    policies = [
        # A user can accept a group invite sent to him or her.
        policies.user.invite.UserReceivedInvite
    ]


class RejectGroupInvite(UserToGroupInviteAction):
    policies = [
        # A user can reject a group invite sent to him or her.
        policies.user.invite.UserReceivedInvite
    ]