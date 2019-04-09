from ..enforcement import AuthorizationResult
from ..utils import assert_subclass


class Action:
    @classmethod
    def authorize(cls, request):
        print("Action:", cls)
        print("Policies:", cls.policies)
        
        # Evaluate all the policies of this action.
        for policy in cls.policies:
            print("Evaluating policy:", policy)
            try:
                if policy.evaluate(request):
                    return AuthorizationResult.PERMIT
                else:
                    return AuthorizationResult.DENY
            except Exception as error:
                print("Skipping inapplicable action authorization:", error)
        
        # If we get to this point, then none of the policies were applicable.
        return AuthorizationResult.NOT_APPLICABLE
    
    @classmethod
    def assert_attribute_classes(cls, subject, resource, context):
        # Assert the subject attribute's class if available.
        if hasattr(cls, "_subject_class"):
            assert_subclass(subject, cls._subject_class)
        
        # Assert the resource attribute's class if available.
        if hasattr(cls, "_resource_class"):
            assert_subclass(resource, cls._resource_class)
        
        # Assert the context attribute's class if available.
        if hasattr(cls, "_context_class"):
            assert_subclass(resource, cls._context_class)