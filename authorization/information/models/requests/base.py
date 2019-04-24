from ..invites.base import Invite
from authorization.utilities.decorators import classproperty
from authorization.utilities.reflection import get_class_name


# A request is actually just a sub-type of invite.
class Request(Invite):
    """
    Class properties and methods
    """
    
    # This returns the UIDs of all the requests in the database.
    @classproperty
    def all_request_uids(cls):
        return super().all_invite_uids(cls)
    
    # This returns all the requests in the database.
    @classproperty
    def all_requests(cls):
        return super().all_invites(cls)
    
    # Disable the all_invite_uids field from the Invite wrapper.
    @classproperty
    def all_invite_uids(cls):
        raise NotImplementedError(
            "The all_invite_uids field has been disabled for %s!" %
            get_class_name(cls)
        )
    
    # Disable the all_invites field from the Invite wrapper.
    @classproperty
    def all_invites(cls):
        raise NotImplementedError(
            "The all_invites field has been disabled for %s!" %
            get_class_name(cls)
        )