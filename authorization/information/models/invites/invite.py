from ..base import ModelWrapper
from authorization.utilities.decorators import classproperty

# MyAlmanack database (Justin's subsystem)
from database.models import Invite as _Invite


class Invite(ModelWrapper):
    """
    Wrapper-related
    """
    
    _root = _Invite
    
    # This returns the ID of this invite.
    @property
    def uid(self):
        return self._object.invite_id
    
    # This returns an invite in the database given its ID.
    @classmethod
    def from_uid(cls, uid):
        return cls(cls._root.objects.get(invite_id=uid))
    
    """
    Class properties and methods
    """
    
    # This returns all the invites in the database.
    @classproperty
    def all_invites(cls):
        return frozenset(cls(invite) for invite in cls._root.objects.all())