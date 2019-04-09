from ..utilities.wrapper import Wrapper
from ..utilities._class import is_subclass

# MyAlmanack database (Justin's subsystem)
from database.models import Profile#, ContactList

# Django
from django.contrib.auth import get_user_model
User = get_user_model()


class User(Wrapper):
    # {uid: user}
    _cache = {}
    
    def wrap(self, object):
        if isinstance(object, User):
            return object
        elif isinstance(object, Profile):
            # The UID is stored in the username field.
            return User.objects.get(username=object.firebase_id)
    
    @classmethod
    def is_wrappable(cls, object):
        return isinstance(object, (User, Profile))
    
    @classmethod
    def from_uid(cls, uid):
        return cls(User.objects.get(username=uid))
    
    def get_uid(self):
        # The UID is stored in the username field.
        return self._object.username
    
    def get_profile(self):
        return Profile.objects.get(firebase_id=self._object.username)
    
    # This returns a list of users which are contacts to this user.
    def get_contacts(self):
        uids = self.get_profile().contact_list.contact_names
        return [User.from_uid(uid) for uid in uids]