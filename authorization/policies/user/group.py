from authorization.decision import Policy


# This checks whether a user subject is a member of a group resource.
class UserIsGroupMember(Policy):
    @staticmethod
    def evaluate(request):
        return request.subject.uid in request.resource.member_uids


# This checks whether a user resource is a member of a group context.
class UserResourceIsGroupContextMember(Policy):
    @staticmethod
    def evaluate(request):
        return request.resource.uid in request.context.member_uids


# This checks whether a user subject is an administrator of a group resource.
class UserIsGroupAdministrator(Policy):
    @staticmethod
    def evaluate(request):
        return request.subject.uid in request.resource.administrator_uids


# This checks whether a user subject is an administrator of a group context.
class UserIsGroupContextAdministrator(Policy):
    @staticmethod
    def evaluate(request):
        return request.subject.uid in request.context.administrator_uids


# This checks whether a user subject is a member of but not an administrator of
#     a group resource.
class UserIsGroupParticipant(Policy):
    @staticmethod
    def evaluate(request):
        return request.subject.uid in request.resource.participant_uids


# This checks whether a user subject has been invited to a group resource.
class UserIsInvitedToGroup(Policy):
    @staticmethod
    def evaluate(request):
        for received_group_invite in request.subject.received_group_invites:
            if received_group_invite.group_uid == request.resource.uid:
                return True
        return False


# This checks whether a user resource has been invited to a group context.
class UserResourceIsInvitedToGroupContext(Policy):
    @staticmethod
    def evaluate(request):
        for received_group_invite in request.resource.received_group_invites:
            if received_group_invite.group_uid == request.context.uid:
                return True
        return False


# This checks whether a user subject has sent a group request to a group
#     resource.
class UserSentGroupRequest(Policy):
    @staticmethod
    def evaluate(request):
        for sent_group_request in request.subject.sent_group_requests:
            if request.resource.uid in sent_group_request.receiver_uids:
                return True
        return False