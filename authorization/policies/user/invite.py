from authorization.decision import Policy


# This checks whether a user subject is the sender of an invite resource.
class UserSentInvite(Policy):
    @classmethod
    def evaluate(cls, request):
        #return request.resource in request.subject.sent_invites
        if hasattr(request.resource, "senders"):
            return request.subject.uid in request.resource.sender_uids
        else:
            return request.resource.sender_uid == request.subject.uid


# This checks whether a user subject is a receiver of an invite resource.
class UserReceivedInvite(Policy):
    @classmethod
    def evaluate(cls, request):
        #return request.resource in request.subject.received_invites
        if hasattr(request.resource, "receivers"):
            return request.subject.uid in request.resource.receiver_uids
        else:
            return request.resource.receiver_uid == request.subject.uid