from .model import Model
from .user import User
from .group import Group
from .event import Event
from ..utilities.decorators import classproperty

# MyAlmanack database (Justin's subsystem)
from database.models import (
    Invite as _Invite,
    UserRequest as _UserInvite,
    GroupInvite as _GroupInvite,
    EventInvite as _EventInvite,
    Profile as _Profile,
    ContactList as _ContactList
)


class Invite(Model):
    """
    Wrapper-related
    """
    
    _root = _Invite
    
    # This returns the ID of this invite.
    @property
    def uid(self):
        return self._object.invite_id
    
    # This returns an invite in the database given its ID.
    @classmethod
    def from_uid(cls, uid):
        return cls(cls._root.objects.get(invite_id=uid))
    
    """
    Class properties and methods
    """
    
    # This returns all the invites in the database.
    @classproperty
    def all_invites(cls):
        return frozenset(cls(invite) for invite in cls._root.objects.all())


# One-to-one
class UserInvite(Invite):
    """
    Wrapper-related
    """
    
    _root = _UserInvite
    
    """
    Instance properties and methods
    """
    
    # This returns the sender of this user invite.
    @property
    def sender(self):
        return User.from_uid(self._object.sender_id)
    
    # This returns the receiver of this user invite.
    @property
    def receiver(self):
        return User.from_uid(self._object.receiver_id)


# One-to-many
class GroupInvite(Invite):
    """
    Wrapper-related
    """
    
    _root = _GroupInvite
    
    """
    Instance properties and methods
    """
    
    # This returns the sender of this group invite.
    @property
    def sender(self):
        return Group.from_uid(self._object.group_name)
    
    # This returns the receivers of this group invite.
    @property
    def receivers(self):
        return frozenset(
            User.from_uid(uid) for uid in self._object.invitee_list
        )


# One-to-many
class EventInvite(Invite):
    """
    Wrapper-related
    """
    
    _root = _EventInvite
    
    """
    Instance properties and methods
    """
    
    # This returns the sender of this event invite.
    @property
    def sender(self):
        event_id = self.uid
        for contact_list in _ContactList.objects.all():
            if event_id in contact_list.sent_event_invites:
                return User(_Profile.objects.get(
                    contact_list=contact_list.contact_list_id
                ))
    
    # This returns the receivers of this event invite.
    @property
    def receivers(self):
        return frozenset(
            User.from_uid(uid) for uid in self._object.invited_users
        )