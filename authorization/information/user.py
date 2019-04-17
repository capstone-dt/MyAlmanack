from ..utilities.wrapper import Wrapper
from ..utilities.decorators import classproperty
from ..utilities.reflection import is_subclass

# MyAlmanack database (Justin's subsystem)
from database.models import Profile as _Profile


class User(Wrapper):
    """
    Wrapper-related
    """
    
    def wrap(self, object):
        _User = self.user_model
        if isinstance(object, _User):
            return object
        elif isinstance(object, Profile):
            return _User.objects.get(username=object.firebase_id)
    
    @classmethod
    def is_wrappable(cls, object):
        return isinstance(object, (cls.user_model, _Profile))
    
    """
    Miscellaneous
    """
    
    @classmethod
    def from_uid(cls, uid):
        return cls(cls.user_model.objects.get(username=uid))
    
    @classproperty
    def all_users(cls):
        return frozenset(cls(profile) for profile in _Profile.objects.all())
    
    @classproperty
    def user_model(cls):
        if not hasattr(cls, "_user_model"):
            from django.contrib.auth import get_user_model
            cls._user_model = get_user_model()
        return cls._user_model
    
    """
    Instance methods
    """
    
    def __eq__(self, other):
        return isinstance(other, User) and self.uid == other.uid
    
    @property
    def uid(self):
        return self._object.username
    
    @property
    def profile(self):
        return _Profile.objects.get(firebase_id=self._object.username)
    
    # This returns a list of users which are contacts to this user.
    @property
    def contacts(self):
        contact_ids = self.profile.contact_list.contact_names
        return frozenset(User.from_uid(uid) for uid in contact_ids)
    
    @property
    def groups(self):
        from .group import Group
        return frozenset(
            group for group in Group.all_groups if group.contains_user(self)
        )
    
    @property
    def events(self):
        from .event import Event
        return frozenset(
            event for event in Event.all_events if event.contains_user(self)
        )
    
    @property
    def sent_invites(self):
        return (
            self.sent_user_invites
            & self.sent_group_invites
            & self.sent_event_invites
        )
    
    @property
    def received_invites(self):
        return (
            self.received_user_invites
            & self.received_group_invites
            & self.received_event_invites
        )
    
    @property
    def sent_user_invites(self):
        from .invite import UserInvite
        return frozenset(
            invite for invite in UserInvite.all_invites
            if invite.sender == self
        )
    
    @property
    def received_user_invites(self):
        from .invite import UserInvite
        return frozenset(
            invite for invite in UserInvite.all_invites
            if self in invite.receivers
        )
    
    @property
    def sent_group_invites(self):
        from .invite import GroupInvite
        return frozenset(
            invite for invite in GroupInvite.all_invites
            if self in invite.sender.administrators
        )
    
    @property
    def received_group_invites(self):
        from .invite import GroupInvite
        return frozenset(
            invite for invite in GroupInvite.all_invites
            if self in invite.receivers
        )
    
    @property
    def sent_event_invites(self):
        from .invite import EventInvite
        return frozenset(
            invite for invite in EventInvite.all_invites
            if invite.sender == self
        )
    
    @property
    def received_event_invites(self):
        from .invite import EventInvite
        return frozenset(
            invite for invite in EventInvite.all_invites
            if self in invite.receivers
        )