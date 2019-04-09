from ..utilities.wrapper import Wrapper
from ..utilities._class import is_subclass

# MyAlmanack database (Justin's subsystem)
#from database.models import Profile, ContactList


# STUB
class ContactList:
    def __init__(self, uids):
        self.contact_names = uids

class Profile:
    def __init__(self, firebase_id):
        self.firebase_id = firebase_id
        self.contact_list = ContactList([
            firebase_id
        ])


class User(Wrapper):
    """
    Wrapper-related
    """
    
    def wrap(self, object):
        User = self.get_user_model()
        if isinstance(object, User):
            return object
        elif isinstance(object, Profile):
            # The UID is stored in the username field.
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
        # The UID is stored in the username field.
        return self._object.username
    
    def get_profile(self):
        #return Profile.objects.get(firebase_id=self._object.username)
        return Profile(firebase_id=self._object.username) # STUBBED
    
    # This returns a list of users which are contacts to this user.
    def get_contacts(self):
        uids = self.get_profile().contact_list.contact_names
        return [User.from_uid(uid) for uid in uids]