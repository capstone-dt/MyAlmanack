from .base import ModelWrapper
from authorization.utilities.decorators import classproperty

# MyAlmanack database (Justin's subsystem)
from database.models import Profile as _Profile

# Django
from django.contrib.auth import get_user_model
_User = get_user_model()


class User(ModelWrapper):
    """
    Wrapper-related
    """
    
    def wrap(self, object):
        if isinstance(object, _User):
            # Django's User model - keep it as is
            return object
        elif isinstance(object, _Profile):
            # Justin's Profile model - convert to Django's User model
            return _User.objects.get(username=object.firebase_id)
    
    @classmethod
    def is_wrappable(cls, object):
        return isinstance(object, (_User, _Profile))
    
    # This returns the ID of this user.
    @property
    def uid(self):
        return self._object.username
    
    # This returns a user in the database given their ID.
    @classmethod
    def from_uid(cls, uid):
        return cls(_User.objects.get(username=uid))
    
    """
    Class properties and methods
    """
    
    # This returns all the users in the database.
    @classproperty
    def all_users(cls):
        return frozenset(cls(profile) for profile in _Profile.objects.all())
    
    """
    Instance properties and methods
    """
    
    # This returns the Profile model of this user.
    @property
    def profile(self):
        return _Profile.objects.get(firebase_id=self._object.username)
    
    # This returns a set of users which are contacts to this user.
    @property
    def contacts(self):
        contact_ids = self.profile.contact_list.contact_names
        return frozenset(User.from_uid(uid) for uid in contact_ids)
    
    # This returns a set of groups that this user is a member of.
    @property
    def groups(self):
        from .group import Group
        return frozenset(
            group for group in Group.all_groups if self in group.members
        )
    
    # This returns a set of events that this user is a member of.
    @property
    def events(self):
        from .event import Event
        return frozenset(
            event for event in Event.all_events if self in event.members
        )
    
    # This returns a set of invites that this user has sent or received.
    @property
    def invites(self):
        return self.user_invites | self.group_invites | self.event_invites
    
    # This returns a set of user invites that this user has sent or received.
    @property
    def user_invites(self):
        return self.sent_user_invites | self.received_user_invites
    
    # This returns a set of group invites that this user has sent or received.
    @property
    def group_invites(self):
        return self.sent_group_invites | self.received_group_invites
    
    # This returns a set of event invites that this user has sent or received.
    @property
    def event_invites(self):
        return self.sent_event_invites | self.received_event_invites
    
    # This returns a set of invites that this user has sent.
    @property
    def sent_invites(self):
        return (
            self.sent_user_invites
            | self.sent_group_invites
            | self.sent_event_invites
        )
    
    # This returns a set of invites that this user has received.
    @property
    def received_invites(self):
        return (
            self.received_user_invites
            | self.received_group_invites
            | self.received_event_invites
        )
    
    # This returns a set of user invites that this user has sent.
    @property
    def sent_user_invites(self):
        from .invites.user_invite import UserInvite
        return frozenset(
            invite for invite in UserInvite.all_invites
            if invite.sender == self
        )
    
    # This returns a set of user invites that this user has received.
    @property
    def received_user_invites(self):
        from .invites.user_invite import UserInvite
        return frozenset(
            invite for invite in UserInvite.all_invites
            if self in invite.receivers
        )
    
    # This returns a set of group invites that this user has sent.
    @property
    def sent_group_invites(self):
        from .invites.group_invite import GroupInvite
        return frozenset(
            invite for invite in GroupInvite.all_invites
            if self in invite.sender.administrators
        )
    
    # This returns a set of group invites that this user has received.
    @property
    def received_group_invites(self):
        from .invites.group_invite import GroupInvite
        return frozenset(
            invite for invite in GroupInvite.all_invites
            if self in invite.receivers
        )
    
    # This returns a set of event invites that this user has sent.
    @property
    def sent_event_invites(self):
        from .invites.event_invite import EventInvite
        return frozenset(
            invite for invite in EventInvite.all_invites
            if invite.sender == self
        )
    
    # This returns a set of event invites that this user has received.
    @property
    def received_event_invites(self):
        from .invites.event_invite import EventInvite
        return frozenset(
            invite for invite in EventInvite.all_invites
            if self in invite.receivers
        )