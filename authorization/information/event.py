from .user import User
from ..utilities.decorators import classproperty
from ..utilities.wrapper import Wrapper

# MyAlmanack database (Justin's subsystem)
from database.models import Event as _Event


class Event(Wrapper):
    """
    Wrapper-related
    """
    
    _root = _Event
    
    """
    Miscellaneous
    """
    
    @classmethod
    def from_uid(cls, uid):
        return cls(_Event.objects.get(event_id=uid))
    
    @classproperty
    def all_events(cls):
        return frozenset(cls(event) for event in _Event.objects.all())
    
    """
    Instance methods
    """
    
    def __eq__(self, other):
        return isinstance(other, Event) and self.uid == other.uid
    
    @property
    def uid(self):
        return self._object.event_id
    
    # This returns a list of members who are members of this event.
    @property
    def members(self):
        return frozenset(
            User.from_uid(uid) for uid in self._object.participating_users
        )
    
    # This returns a list of administrators who are members of this event.
    @property
    def administrators(self):
        return frozenset(
            user for user in self.members
            if user.uid in self._object.event_admins
        )
    
    # This returns whether a user is a member or an administrator of this event.
    def contains_user(self, user):
        return user in self.members or user in self.administrators
    
    @property
    def whitelisted_users(self):
        return frozenset(
            User.from_uid(uid) for uid in self._object.whitelist
        )
    
    @property
    def blacklisted_users(self):
        return frozenset(
            User.from_uid(uid) for uid in self._object.blacklist
        )