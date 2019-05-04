from authorization.decision import Policy


# This checks whether a user subject is a member of an event resource.
class UserIsEventMember(Policy):
    @staticmethod
    def evaluate(request):
        return request.subject.uid in request.resource.member_uids


# This checks whether a user resource is a member of an event context.
class UserResourceIsEventContextMember(Policy):
    @staticmethod
    def evaluate(request):
        return request.resource.uid in request.context.member_uids


# This checks whether a user subject is the creator of an event resource.
class UserIsEventCreator(Policy):
    @staticmethod
    def evaluate(request):
        return request.subject.uid == request.resource.creator_uid


# This checks whether a user subject is the creator of an event context.
class UserIsEventContextCreator(Policy):
    @staticmethod
    def evaluate(request):
        return request.subject.uid == request.context.creator_uid


# This checks whether a user subject is an administrator of an event resource.
class UserIsEventAdministrator(Policy):
    @staticmethod
    def evaluate(request):
        return request.subject.uid in request.resource.administrator_uids


# This checks whether a user subject is an administrator of an event context.
class UserIsEventContextAdministrator(Policy):
    @staticmethod
    def evaluate(request):
        return request.subject.uid in request.context.administrator_uids


# This checks whether a user subject is a participant of an event resource.
class UserIsEventParticipant(Policy):
    @staticmethod
    def evaluate(request):
        return request.subject.uid in request.resource.participant_uids


# This checks whether a user subject is a whitelisted user of an event resource.
class UserIsInEventWhitelist(Policy):
    @staticmethod
    def evaluate(request):
        return request.subject.uid in request.resource.whitelisted_uids


# This checks whether a user subject is a blacklisted user of an event resource.
class UserIsInEventBlacklist(Policy):
    @staticmethod
    def evaluate(request):
        return request.subject.uid in request.resource.blacklisted_uids


# This checks whether a user subject has been invited to an event resource.
class UserIsInvitedToEvent(Policy):
    @staticmethod
    def evaluate(request):
        for received_event_invite in request.subject.received_event_invites:
            if received_event_invite.event_uid == request.resource.uid:
                return True
        return False


# This checks whether a user resource has been invited to an event context.
class UserResourceIsInvitedToEventContext(Policy):
    @staticmethod
    def evaluate(request):
        for received_event_invite in request.resource.received_event_invites:
            if received_event_invite.event_uid == request.context.uid:
                return True
        return False