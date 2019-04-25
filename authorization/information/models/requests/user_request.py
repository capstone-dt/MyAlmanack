from .base import Request
from ..user import User
from authorization.utilities.decorators import classproperty

# MyAlmanack database (Justin's subsystem)
from database.models import UserRequest as _UserRequest


# One-to-one
class UserRequest(Request):
    """
    Wrapper-related
    """
    
    _root = _UserRequest
    
    """
    Instance properties and methods
    """
    
    # This returns the UID of the sender of this user request.
    @property
    def sender_uid(self):
        return self._object.sender_id
    
    # This returns the sender of this user request.
    @property
    def sender(self):
        return User.from_uid(self.sender_uid)
    
    # This returns the UID of the receiver of this user request.
    @property
    def receiver_uid(self):
        return self._object.receiver_id
    
    # This returns the receiver of this user request.
    @property
    def receiver(self):
        return User.from_uid(self.receiver_uid)