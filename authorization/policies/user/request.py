from authorization.decision import Policy


# This checks whether a user subject is the sender of a request resource.
class UserSentRequest(Policy):
    @staticmethod
    def evaluate(request):
        #return request.resource in request.subject.sent_requests
        if hasattr(request.resource, "senders"):
            return request.subject.uid in request.resource.sender_uids
        else:
            return request.resource.sender_uid == request.subject.uid


# This checks whether a user subject is a receiver of a request resource.
class UserReceivedRequest(Policy):
    @staticmethod
    def evaluate(request):
        #return request.resource in request.subject.received_requests
        if hasattr(request.resource, "receivers"):
            return request.subject.uid in request.resource.receiver_uids
        else:
            return request.resource.receiver_uid == request.subject.uid