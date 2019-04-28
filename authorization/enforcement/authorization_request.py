from .enforcement_authority import EnforcementAuthority
from .authorization_result import AuthorizationResult
from ..attributes import Subject, Action, Resource, Context, wrap_attribute
from ..utilities.reflection import get_class_name, assert_subclass


# The AuthorizationRequest class provides a way to create authorization requests
#     using the given attributes, and automatically wraps them using appropriate
#     attribute wrappers so users of the APIs won't have to do it manually.
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
    
    # This calls the enforcement authority to authorize the authorization
    #     request.
    def authorize(self):
        return EnforcementAuthority.authorize(self)
    
    # This calls the authorize() method and checks if the authorization request
    #     is permitted.
    @property
    def permitted(self):
        return self.authorize() == AuthorizationResult.PERMIT
    
    def __str__(self):
        return "%s[subject=%s, action=Action[%s], resource=%s, context=%s]" % (
            get_class_name(self),
            self.subject,
            self.action,
            self.resource,
            self.context
        )