from .decision_authority import DecisionAuthority
from ..attributes import Subject, Action, Object, Context, wrap_attribute
from ..utils import get_class_name, assert_subclass


class AuthorizationRequest:
    def __init__(self, subject, action, object, context={}):
        # Make sure that the given action is a subclass of Action.
        assert_subclass(action, Action)
        self.action = action
        
        # Wrap all other attributes using appropriate wrapper classes.
        self.subject = wrap_attribute(Subject, subject, "subjects")
        self.object = wrap_attribute(Object, object, "objects")
        self.context = wrap_attribute(Context, context, "contexts")
        
        # Check the action's constraints if available.
        # Check if the Action class requires certain Subject, Object, or Context classes.
        
    
    def authorize(self):
        return DecisionAuthority.authorize(self)
    
    @property
    def is_permitted(self):
        return DecisionAuthority.is_permitted(self)
    
    def __str__(self):
        return "%s[subject=%s, action=Action[%s], object=%s, context=%s]" % (
            get_class_name(self),
            self.subject,
            get_class_name(self.action),
            self.object,
            self.context
        )