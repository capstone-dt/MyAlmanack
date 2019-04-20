from ..bounded_actions import UserToEventAction
from authorization import policies


class ViewEvent(UserToEventAction):
    policies = [
        # Anyone can view an event.
        policies.miscellaneous.Tautology
    ]


class EditEvent(UserToEventAction):
    policies = [
        # An event creator can edit an event.
        policies.user.event.UserIsEventCreator,
        
        # An event administrator can edit an event.
        policies.user.event.UserIsEventAdministrator
    ]


class DeleteEvent(UserToEventAction):
    policies = [
        # An event creator can delete an event.
        policies.user.event.UserIsEventCreator
    ]