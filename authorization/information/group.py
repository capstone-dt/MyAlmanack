from .user import User
from ..utilities.wrapper import Wrapper
from ..utilities._class import is_subclass

# MyAlmanack database (Justin's subsystem)
#from database.models import Group as _Group
from .stubs import Group as _Group


class Group(Wrapper):
    """
    Wrapper-related
    """
    
    _root = _Group
    
    """
    Miscellaneous
    """
    
    @classmethod
    def get_all_groups(cls):
        #all_groups = _Group.objects.all()
        all_groups = [_Group("12345"), _Group("67890")] # STUB
        return [cls.from_uid(group.group_name) for group in all_groups]
    
    @classmethod
    def from_uid(cls, uid):
        #return cls(_Group.objects.get(group_name=uid))
        return cls(_Group("12345")) # STUB
    
    """
    Instance methods
    """
    
    def __eq__(self, other):
        return isinstance(other, Group) and self.get_uid() == other.get_uid()
    
    def get_uid(self):
        return self._object.group_name
    
    # This returns a list of members who are members of this group.
    def get_members(self):
        return [User.from_uid(uid) for uid in self._object.group_members]
    
    # This returns a list of administrators who are members of this group.
    def get_administrators(self):
        return [
            user for user in self.get_members()
            if user.get_uid() in self._object.group_admin
        ]
    
    def contains_user(self, user):
        return user in self.get_members()