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
    
    # This returns the sender of this event invite.
    @property
    def sender(self):
        event_id = self.uid
        for contact_list in _ContactList.objects.all():
            if event_id in contact_list.sent_event_invites:
                return User(_Profile.objects.get(
                    contact_list=contact_list.contact_list_id
                ))
    
    # This returns the receivers of this event invite.
    @property
    def receivers(self):
        return User.from_uids(self._object.invited_users)