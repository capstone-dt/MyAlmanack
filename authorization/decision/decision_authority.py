from ..attributes.action import Action
from ..enforcement.authorization_result import AuthorizationResult
from ..utilities.reflection import assert_subclass


class DecisionAuthority:
    @classmethod
    def authorize(cls, request):
        # Make sure that the authorization request's action is an Action class.
        assert_subclass(request.action, Action)
        
        print("Action:", request.action)
        print("Policies:", request.action.policies)
        
        # Evaluate all the policies of this action.
        for policy in request.action.policies:
            print("Evaluating policy:", policy)
            try:
                if policy.evaluate(request):
                    return AuthorizationResult.PERMIT
            except Exception as error:
                print("Inapplicable action authorization policy:", error)
                return AuthorizationResult.NOT_APPLICABLE
        
        # If we get to this point, then none of the policies evaluated to true.
        return AuthorizationResult.DENY
    
    @classmethod
    def is_permitted(cls, request):
        return cls.authorize(request) == AuthorizationResult.PERMIT