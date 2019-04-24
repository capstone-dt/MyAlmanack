from .base import Request
from ..user import User
from ..group import Group
from authorization.utilities.decorators import classproperty

# MyAlmanack database (Justin's subsystem)
from database.models import GroupRequest as _GroupRequest


# One-to-many
class GroupRequest(Request):
    """
    Wrapper-related
    """
    
    _root = _GroupRequest
    
    """
    Instance properties and methods
    """
    
    # This returns the UID of the group of this group request.
    @property
    def group_uid(self):
        return self._object.group_name
    
    # This returns the group of this group request.
    @property
    def group(self):
        return Group.from_uid(self.group_uid)
    
    # This returns the UID of the sender of this group request.
    @property
    def sender_uid(self):
        return self._object.sender.firebase_id
    
    # This returns the sender of this group request.
    @property
    def sender(self):
        return User.from_uid(self.sender_uid)
    
    # This returns the UIDs of the receivers of this group request.
    @property
    def receiver_uids(self):
        return self.group.administrator_uids
    
    # This returns the receivers of this group request.
    @property
    def receivers(self):
        return self.group.administrators