from .decision_authority import DecisionAuthority
from ..attributes import Subject, Action, Resource, Context, wrap_attribute
from ..utils import get_class_name, assert_subclass


class AuthorizationRequest:
    def __init__(self, subject, action, resource, context={}):
        # Make sure that the given action is a subclass of Action.
        assert_subclass(action, Action)
        self.action = action
        
        # Wrap all other attributes using appropriate wrapper classes.
        self.subject = wrap_attribute(Subject, subject, "subjects")
        self.resource = wrap_attribute(Resource, resource, "resources")
        self.context = wrap_attribute(Context, context, "contexts")
        
        # Assert the action's attribute class constraints.
        action.assert_attribute_classes(
            subject=self.subject,
            resource=self.resource,
            context=self.context
        )
    
    def authorize(self):
        return DecisionAuthority.authorize(self)
    
    @property
    def is_permitted(self):
        return DecisionAuthority.is_permitted(self)
    
    def __str__(self):
        return "%s[subject=%s, action=Action[%s], resource=%s, context=%s]" % (
            get_class_name(self),
            self.subject,
            get_class_name(self.action),
            self.resource,
            self.context
        )