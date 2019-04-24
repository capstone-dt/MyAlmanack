from .base import Invite
from ..user import User
from ..group import Group
from authorization.utilities.decorators import classproperty

# MyAlmanack database (Justin's subsystem)
from database.models import GroupInvite as _GroupInvite


# Many-to-many
class GroupInvite(Invite):
    """
    Wrapper-related
    """
    
    _root = _GroupInvite
    
    """
    Instance properties and methods
    """
    
    # This returns the UID of the group of this group invite.
    @property
    def group_uid(self):
        return self._object.group_name
    
    # This returns the group of this group invite.
    @property
    def group(self):
        return Group.from_uid(self.group_uid)
    
    # This returns the UIDs of the senders of this group invite.
    @property
    def sender_uids(self):
        return self.group.administrator_uids
    
    # This returns the senders of this group invite.
    @property
    def senders(self):
        return self.group.administrators
    
    # This returns the UIDs of the receivers of this group invite.
    @property
    def receiver_uids(self):
        return frozenset(self._object.invitee_list)
    
    # This returns the receivers of this group invite.
    @property
    def receivers(self):
        return User.from_uids(self.receiver_uids)