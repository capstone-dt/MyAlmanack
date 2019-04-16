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
                else:
                    return AuthorizationResult.DENY
            except Exception as error:
                print("Unable to evaluate action authorization:", error)
        
        # If we get to this point, then none of the policies were applicable.
        return AuthorizationResult.NOT_APPLICABLE
    
    @classmethod
    def is_permitted(cls, request):
        return cls.authorize(request) == AuthorizationResult.PERMIT