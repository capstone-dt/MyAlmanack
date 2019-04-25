from authorization.decision import Policy


# This checks whether two users are contacts.
class UsersAreContacts(Policy):
    @classmethod
    def evaluate(cls, request):
        return (
            request.subject.uid in request.resource.contact_uids
            and # Just to make sure...
            request.resource.uid in request.subject.contact_uids
        )


# This checks whether two users share a common group together.
class UsersShareCommonGroup(Policy):
    @classmethod
    def evaluate(cls, request):
        return len(request.subject.group_uids & request.resource.group_uids) > 0


# This checks whether a user subject has sent a user request to a user resource.
class UserSentUserRequest(Policy):
    @classmethod
    def evaluate(cls, request):
        for sent_user_request in request.subject.sent_user_requests:
            if sent_user_request.receiver_uid == request.resource.uid:
                return True
        return False