from ..bounded_actions import UserToEventAction
from authorization import policies


class ViewEventCalendar(UserToEventAction):
    policies = [
        # A user who is an event's member can view the event's calendar.
        policies.user.event.UserIsEventMember
    ]


class EditEventCalendar(UserToEventAction):
    policies = [
        # A user who is an event's creator can edit the event's calendar.
        policies.user.event.UserIsEventCreator,
        
        # A user who is an event's administrator can edit the event's calendar.
        policies.user.group.UserIsGroupAdministrator
    ]