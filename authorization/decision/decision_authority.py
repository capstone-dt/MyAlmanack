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
        all_inapplicable = True
        for policy in request.action.policies:
            print("Evaluating policy:", policy)
            try:
                if policy.evaluate(request):
                    return AuthorizationResult.PERMIT
                else:
                    all_inapplicable = False
            except Exception as error:
                print("Inapplicable policy:", error)
        
        # If we get to this point, then none of the policies evaluated to true.
        if all_inapplicable:
            # If every policy threw an error, then the authorization request is
            #     inapplicable.
            return AuthorizationResult.NOT_APPLICABLE
        else:
            # Otherwise, at least one policy evaluated to false.
            return AuthorizationResult.DENY