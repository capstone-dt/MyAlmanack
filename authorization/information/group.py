from .user import User
from ..utilities.wrapper import Wrapper
from ..utilities.decorators import classproperty

# MyAlmanack database (Justin's subsystem)
from database.models import Group as _Group


class Group(Wrapper):
    """
    Wrapper-related
    """
    
    _root = _Group
    
    """
    Miscellaneous
    """
    
    @classmethod
    def from_uid(cls, uid):
        return cls(_Group.objects.get(group_name=uid))
    
    @classproperty
    def all_groups(cls):
        return frozenset(cls(group) for group in _Group.objects.all())
    
    """
    Instance methods
    """
    
    def __eq__(self, other):
        return isinstance(other, Group) and self.uid == other.uid
    
    def __hash__(self):
        return hash((str(self), self.uid))
    
    @property
    def uid(self):
        return self._object.group_name
    
    # This returns a list of members who are members of this group.
    @property
    def members(self):
        return frozenset(
            User.from_uid(uid) for uid in self._object.group_members
        )
    
    # This returns a list of administrators who are members of this group.
    @property
    def administrators(self):
        return frozenset(
            user for user in self.members
            if user.uid in self._object.group_admin
        )
    
    # This returns whether a user is a member or an administrator of this group.
    def contains_user(self, user):
        return user in self.members or user in self.administrators