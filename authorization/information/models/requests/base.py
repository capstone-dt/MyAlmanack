from ..base import ModelWrapper
from authorization.utilities.decorators import classproperty

# MyAlmanack database (Justin's subsystem)
from database.models import Invite as _Invite


# The Request model wrapper class encapsulates a part of the database model for
#     Invite.
# See the Invite model wrapper for the other part.
class Request(ModelWrapper):
    """
    Wrapper-related
    """
    
    # A request is actually just a sub-type of invite.
    _root = _Invite
    
    # This returns the UID of this invite.
    @property
    def uid(self):
        return self._object.invite_id
    
    # This returns an invite in the database given its UID.
    @classmethod
    def from_uid(cls, uid):
        return cls(cls._root.objects.get(invite_id=uid))
    
    """
    Class properties and methods
    """
    
    # This returns the UIDs of all the invites in the database.
    @classproperty
    def all_request_uids(cls):
        return frozenset(invite.invite_id for invite in cls._root.objects.all())
    
    # This returns all the invites in the database.
    @classproperty
    def all_requests(cls):
        return frozenset(cls(invite) for invite in cls._root.objects.all())