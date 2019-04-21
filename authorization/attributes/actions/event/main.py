from ..bounded_actions import UserToEventAction
from authorization import policies


class ViewEvent(UserToEventAction):
    policies = [
        # Anyone can view an event.
        policies.miscellaneous.Tautology
    ]


class EditEvent(UserToEventAction):
    policies = [
        # A user who is an event's creator can edit the event.
        policies.user.event.UserIsEventCreator,
        
        # A user who is an event's administrator can edit an event.
        policies.user.event.UserIsEventAdministrator
    ]


class DeleteEvent(UserToEventAction):
    policies = [
        # A user who is an event's creator can delete the event.
        policies.user.event.UserIsEventCreator
    ]