from .base import ModelWrapper
from .user import User
from authorization.utilities.decorators import classproperty

# MyAlmanack database (Justin's subsystem)
from database.models import Event as _Event


class Event(ModelWrapper):
    """
    Wrapper-related
    """
    
    _root = _Event
    
    # This returns the ID of this event.
    @property
    def uid(self):
        return self._object.event_id
    
    # This returns an event in the database given its ID.
    @classmethod
    def from_uid(cls, uid):
        return cls(cls._root.objects.get(event_id=uid))
    
    """
    Class properties and methods
    """
    
    # This returns all the events in the database.
    @classproperty
    def all_events(cls):
        return frozenset(cls(event) for event in cls._root.objects.all())
    
    """
    Instance properties and methods
    """
    
    # This returns a list of users who are members of this event.
    # Members encompass the event's creator, administrators, and participants.
    # Be aware that not all event members "participate" in an event!
    @property
    def members(self):
        return frozenset((creator,)) | self.administrators | self.participants
    
    # This returns the creator of this event.
    @property
    def creator(self):
        return User.from_uid(self._object.event_creator_firebase)
    
    # This returns a list of users who are administrators of this event.
    @property
    def administrators(self):
        return frozenset(
            User.from_uid(uid) for uid in self._object.event_admins
        )
    
    # This returns a list of users who are participants of this event.
    @property
    def participants(self):
        return frozenset(
            User.from_uid(uid) for uid in self._object.participating_users
        )
    
    # This returns a list of users who are whitelisted for this event.
    @property
    def whitelisted_users(self):
        return frozenset(
            User.from_uid(uid) for uid in self._object.whitelist
        )
    
    # This returns a list of users who are blacklisted for this event.
    @property
    def blacklisted_users(self):
        return frozenset(
            User.from_uid(uid) for uid in self._object.blacklist
        )