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
    
    # This returns the sender of this group invite.
    @property
    def sender(self):
        return Group.from_uid(self._object.group_name)
    
    # This returns the receivers of this group invite.
    @property
    def receivers(self):
        return User.from_uids(self._object.invitee_list)