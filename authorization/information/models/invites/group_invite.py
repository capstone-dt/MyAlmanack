from .invite import Invite
from ..user import User
from ..group import Group
from authorization.utilities.decorators import classproperty

# MyAlmanack database (Justin's subsystem)
from database.models import GroupInvite as _GroupInvite


class GroupInvite(Invite):
    """
    Wrapper-related
    """
    
    _root = _GroupInvite
    
    """
    Instance properties and methods
    """
    
    # This returns the UID of the sender of this group invite.
    @property
    def sender_uid(self):
        return self._object.group_name
    
    # This returns the sender of this group invite.
    @property
    def sender(self):
        return Group.from_uid(self.sender_uid)
    
    # This returns the UIDs of the receivers of this group invite.
    @property
    def receiver_uids(self):
        return frozenset(self._object.invitee_list)
    
    # This returns the receivers of this group invite.
    @property
    def receivers(self):
        return User.from_uids(self.receiver_uids)