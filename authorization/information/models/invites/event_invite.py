from .invite import Invite
from ..user import User
from authorization.utilities.decorators import classproperty

# MyAlmanack database (Justin's subsystem)
from database.models import (
    EventInvite as _EventInvite,
    Profile as _Profile,
    ContactList as _ContactList
)


class EventInvite(Invite):
    """
    Wrapper-related
    """
    
    _root = _EventInvite
    
    """
    Instance properties and methods
    """
    
    # This returns the UID of the sender of this event invite.
    @property
    def sender_uid(self):
        event_id = self.uid
        for contact_list in _ContactList.objects.all():
            if event_id in contact_list.sent_event_invites:
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