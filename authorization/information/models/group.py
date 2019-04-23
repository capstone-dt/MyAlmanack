from .base import ModelWrapper
from .user import User
from authorization.utilities.decorators import classproperty

# MyAlmanack database (Justin's subsystem)
from database.models import Group as _Group


class Group(ModelWrapper):
    """
    Wrapper-related
    """
    
    _root = _Group
    
    # This returns the UID of this group.
    @property
    def uid(self):
        return self._object.group_name
    
    # This returns a group in the database given its UID.
    @classmethod
    def from_uid(cls, uid):
        return cls(cls._root.objects.get(group_name=uid))
    
    """
    Class properties and methods
    """
    
    # This returns the UIDs of all the groups in the database.
    @classproperty
    def all_group_uids(cls):
        return frozenset(group.group_name for group in cls._root.objects.all())
    
    # This returns all the groups in the database.
    @classproperty
    def all_groups(cls):
        return frozenset(cls(group) for group in cls._root.objects.all())
    
    """
    Instance properties and methods
    """
    
    # This returns a set of UIDs of users who are members of this group.
    @property
    def member_uids(self):
        return frozenset(self._object.group_members)
    
    # This returns a set of users who are members of this group.
    @property
    def members(self):
        return User.from_uids(self.member_uids)
    
    # This returns a set of UIDs of users who are administrators of this group.
    @property
    def administrator_uids(self):
        return frozenset(self._object.group_admin)
    
    # This returns a set of users who are administrators of this group.
    @property
    def administrators(self):
        return User.from_uids(self.administrator_uids)
    
    # This returns a set of UIDs of users who are participants of this group.
    @property
    def participant_uids(self):
        return self.member_uids - self.administrator_uids
    
    # This returns a set of users who are participants of this group.
    @property
    def participants(self):
        return User.from_uids(self.participant_uids)