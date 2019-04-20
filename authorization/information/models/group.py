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
    
    # This returns the ID of this group.
    @property
    def uid(self):
        return self._object.group_name
    
    # This returns a group in the database given its ID.
    @classmethod
    def from_uid(cls, uid):
        return cls(cls._root.objects.get(group_name=uid))
    
    """
    Class properties and methods
    """
    
    # This returns all the groups in the database.
    @classproperty
    def all_groups(cls):
        return frozenset(cls(group) for group in cls._root.objects.all())
    
    """
    Instance properties and methods
    """
    
    # This returns a list of users who are members of this group.
    @property
    def members(self):
        return frozenset(
            User.from_uid(uid) for uid in self._object.group_members
        )
    
    # This returns a list of users who are administrators of this group.
    @property
    def administrators(self):
        return frozenset(
            User.from_uid(uid) for uid in self._object.group_admin
        )
    
    # This returns a list of users who are members but are not administrators of
    #     this group.
    @property
    def participants(self):
        return self.members - self.administrators