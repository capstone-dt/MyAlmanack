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
            # Justin's Profile model - convert it to Django's User model
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
    
    # This returns a set of users in the database given their IDs.
    @classmethod
    def from_uids(cls, uids):
        return frozenset(cls.from_uid(uid) for uid in uids)
    
    """
    Class properties and methods
    """
    
    # This returns the UIDs of all the users in the database.
    @classproperty
    def all_user_uids(cls):
        return frozenset(
            profile.firebase_id for profile in _Profile.objects.all()
        )
    
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
    
    # This returns a set of UIDs of users who are contacts with this users.
    @property
    def contact_uids(self):
        # contact_names might be blank, so return an empty tuple in that case.
        return frozenset(self.profile.contact_list.contact_names or ())
    
    # This returns a set of users who are contacts with this user.
    @property
    def contacts(self):
        return User.from_uids(self.contact_uids)
    
    # This returns a set of groups that this user is a member of.
    @property
    def groups(self):
        from .group import Group
        return frozenset(
            group for group in Group.all_groups if self.uid in group.member_uids
        )
    
    # This returns a set of events that this user is a member of.
    @property
    def events(self):
        from .event import Event
        return frozenset(
            event for event in Event.all_events if self.uid in event.member_uids
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
            if invite.sender_uid == self.uid
        )
    
    # This returns a set of user invites that this user has received.
    @property
    def received_user_invites(self):
        from .invites.user_invite import UserInvite
        return frozenset(
            invite for invite in UserInvite.all_invites
            if self.uid in invite.receiver_uids
        )
    
    # This returns a set of group invites that this user has sent.
    @property
    def sent_group_invites(self):
        from .invites.group_invite import GroupInvite
        return frozenset(
            invite for invite in GroupInvite.all_invites
            if self.uid in invite.sender_uids
        )
    
    # This returns a set of group invites that this user has received.
    @property
    def received_group_invites(self):
        from .invites.group_invite import GroupInvite
        return frozenset(
            invite for invite in GroupInvite.all_invites
            if self.uid in invite.receiver_uids
        )
    
    # This returns a set of event invites that this user has sent.
    @property
    def sent_event_invites(self):
        from .invites.event_invite import EventInvite
        return frozenset(
            invite for invite in EventInvite.all_invites
            if invite.sender_uid == self.uid
        )
    
    # This returns a set of event invites that this user has received.
    @property
    def received_event_invites(self):
        from .invites.event_invite import EventInvite
        return frozenset(
            invite for invite in EventInvite.all_invites
            if self.uid in invite.receiver_uids
        )