from .invite import Invite
from ..user import User
from authorization.utilities.decorators import classproperty

# MyAlmanack database (Justin's subsystem)
from database.models import UserRequest as _UserInvite


class UserInvite(Invite):
    """
    Wrapper-related
    """
    
    _root = _UserInvite
    
    """
    Instance properties and methods
    """
    
    # This returns the UID of the sender of this user invite.
    @property
    def sender_uid(self):
        return self._object.sender_id
    
    # This returns the sender of this user invite.
    @property
    def sender(self):
        return User.from_uid(self.sender_uid)
    
    # This returns the UID of the receiver of this user invite.
    @property
    def receiver_uid(self):
        return self._object.receiver_id
    
    # This returns the receiver of this user invite.
    @property
    def receiver(self):
        return User.from_uid(self.receiver_uid)