from ..utilities.wrapper import Wrapper
from ..utilities.reflection import is_subclass

# MyAlmanack database (Justin's subsystem)
#from database.models import Profile, ContactList
from .stubs import Profile, ContactList


class User(Wrapper):
    """
    Wrapper-related
    """
    
    def wrap(self, object):
        User = self.get_user_model()
        if isinstance(object, User):
            return object
        elif isinstance(object, Profile):
            return User.objects.get(username=object.firebase_id)
    
    @classmethod
    def is_wrappable(cls, object):
        return isinstance(object, (cls.get_user_model(), Profile))
    
    """
    Miscellaneous
    """
    
    @classmethod
    def get_user_model(cls):
        if not hasattr(cls, "_user_model"):
            from django.contrib.auth import get_user_model
            cls._user_model = get_user_model()
        return cls._user_model
    
    @classmethod
    def from_uid(cls, uid):
        return cls(cls.get_user_model().objects.get(username=uid))
    
    """
    Instance methods
    """
    
    def __eq__(self, other):
        return isinstance(other, User) and self.get_uid() == other.get_uid()
    
    def get_uid(self):
        return self._object.username
    
    def get_profile(self):
        #return Profile.objects.get(firebase_id=self._object.username)
        return Profile(firebase_id=self._object.username) # STUB
    
    # This returns a list of users which are contacts to this user.
    def get_contacts(self):
        contact_ids = self.get_profile().contact_list.contact_names
        return [User.from_uid(uid) for uid in contact_ids]
    
    def get_groups(self):
        from .group import Group
        all_groups = Group.get_all_groups()
        return [group for group in all_groups if group.contains_user(self)]