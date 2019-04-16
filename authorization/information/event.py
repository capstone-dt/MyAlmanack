from .user import User
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
    
    @classmethod
    def get_all_events(cls):
        return frozenset(
            cls.from_uid(event.event_id) for event in _Event.objects.all()
        )
    
    """
    Instance methods
    """
    
    def __eq__(self, other):
        return isinstance(other, Event) and self.get_uid() == other.get_uid()
    
    def get_uid(self):
        return self._object.event_id
    
    # This returns a list of members who are members of this event.
    def get_members(self):
        return frozenset(
            User.from_uid(uid) for uid in self._object.participating_users
        )
    
    # This returns a list of administrators who are members of this event.
    def get_administrators(self):
        return frozenset(
            user for user in self.get_members()
            if user.get_uid() in self._object.event_admins
        )
    
    # This returns whether a user is a member or an administrator of this event.
    def contains_user(self, user):
        return (
            user in self.get_members() or user in self.get_administrators()
        )
    
    def get_whitelisted_users(self):
        return frozenset(
            User.from_uid(uid) for uid in self._object.whitelist
        )
    
    def get_blacklisted_users(self):
        return frozenset(
            User.from_uid(uid) for uid in self._object.blacklist
        )