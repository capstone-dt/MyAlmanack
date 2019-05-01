from .base import ModelWrapper
from .user import User
from authorization.utilities.decorators import classproperty

# MyAlmanack database (Justin's subsystem)
from database.models import Event as _Event, RepeatEvent as _RepeatEvent


# The Event model wrapper class encapsulates the database model for Event.
class Event(ModelWrapper):
    """
    Wrapper-related
    """

    @staticmethod
    def is_wrappable(object):
        return isinstance(object, (_Event, _RepeatEvent))
    
    # This returns the UID of this event.
    @property
    def uid(self):
        return self._object.event_id
    
    # This returns an event in the database given its UID.
    @classmethod
    def from_uid(cls, uid):
        try:
            return cls(_Event.objects.get(event_id=uid))
        except _Event.DoesNotExist:
            return cls(_RepeatEvent.objects.get(event_id=uid))
    
    """
    Class properties and methods
    """
    
    # This returns the UIDs of all the events in the database.
    @classproperty
    def all_event_uids(cls):
        return (
            frozenset(event.event_id for event in _Event.objects.all())
            | frozenset(event.event_id for event in _RepeatEvent.objects.all())
        )
    
    # This returns all the events in the database.
    @classproperty
    def all_events(cls):
        return (
            frozenset(cls(event) for event in _Event.objects.all())
            | frozenset(cls(event) for event in _RepeatEvent.objects.all())
        )
    
    """
    Instance properties and methods
    """

    # This returns whether this event is repeating or not.
    @property
    def repeating(self):
        return isinstance(self._object, _RepeatEvent)
    
    # This returns a set of UIDs of users who are members of this event.
    # Members encompass the event's creator, administrators, and participants.
    # Be aware that not all event members "participate" in an event!
    @property
    def member_uids(self):
        return (
            frozenset((self.creator_uid,))
            | self.administrator_uids
            | self.participant_uids
        )
    
    # This returns a set of users who are members of this event.
    @property
    def members(self):
        return User.from_uids(self.member_uids)
    
    # This returns the UID of the creator of this event.
    @property
    def creator_uid(self):
        return self._object.event_creator_firebase
    
    # This returns the creator of this event.
    @property
    def creator(self):
        return User.from_uid(self.creator_uid)
    
    # This returns a set of UIDs of users who are administrators of this event.
    @property
    def administrator_uids(self):
        return frozenset(self._object.event_admins)
    
    # This returns a set of users who are administrators of this event.
    @property
    def administrators(self):
        return User.from_uids(self.administrator_uids)
    
    # This returns a set of UIDs of users who are participants of this event.
    @property
    def participant_uids(self):
        return frozenset(self._object.participating_users)
    
    # This returns a set of users who are participants of this event.
    @property
    def participants(self):
        return User.from_uids(self.participant_uids)
    
    # This returns a set of UIDs of users who are whitelisted for this event.
    @property
    def whitelisted_uids(self):
        return frozenset(self._object.whitelist)
    
    # This returns a set of users who are whitelisted for this event.
    @property
    def whitelisted_users(self):
        return User.from_uids(self.whitelisted_uids)
    
    # This returns a set of UIDs of users who are blacklisted for this event.
    @property
    def blacklisted_uids(self):
        return frozenset(self._object.blacklist)
    
    # This returns a set of users who are blacklisted for this event.
    @property
    def blacklisted_users(self):
        return User.from_uids(self.blacklisted_uids)