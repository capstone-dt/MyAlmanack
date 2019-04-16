from ..attributes.action import Action
from ..enforcement.authorization_result import AuthorizationResult
from ..utilities.reflection import get_class_name, assert_subclass


class DecisionAuthority:
    @classmethod
    def authorize(cls, request):
        # Extract the action from the authorization request and make sure that
        #     it is an Action class object.
        action = request.action
        assert_subclass(action, Action)
        
        # Make sure that policies have been provided by the action.
        if not hasattr(action, "policies"):
            raise NotImplementedError(
                "The %s action has not provided any policies to evaluate!" %
                get_class_name(action)
            )
        
        print("Action:", action)
        print("Policies:", action.policies)
        
        # Evaluate all the policies of this action.
        for policy in action.policies:
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