from .base import Invite
from ..user import User
from authorization.utilities.decorators import classproperty

# MyAlmanack database (Justin's subsystem)
from database.models import (
    EventInvite as _EventInvite,
    Profile as _Profile,
    ContactList as _ContactList
)


# One-to-many
class EventInvite(Invite):
    """
    Wrapper-related
    """
    
    _root = _EventInvite
    
    """
    Instance properties and methods
    """
    
    # This returns the UID of the event of this event invite.
    @property
    def event_uid(self):
        return self._object.event_id
    
    # This returns the event of this event invite.
    @property
    def event(self):
        return Event.from_uid(self.event_uid)
    
    # This returns the UID of the sender of this event invite.
    @property
    def sender_uid(self):
        for contact_list in _ContactList.objects.all():
            if self.uid in contact_list.sent_event_invites:
                return _Profile.objects.get(
                    contact_list=contact_list.contact_list_id
                ).firebase_id
    
    # This returns the sender of this event invite.
    @property
    def sender(self):
        return User.from_uid(self.sender_uid)
    
    # This returns the UIDs of the receivers of this event invite.
    @property
    def receiver_uids(self):
        return self._object.invited_users
    
    # This returns the receivers of this event invite.
    @property
    def receivers(self):
        return User.from_uids(self.receiver_uids)