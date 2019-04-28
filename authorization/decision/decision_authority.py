from ..enforcement import AuthorizationRequest, AuthorizationResult
from ..attributes.action import Action
from ..utilities.reflection import assert_subclass

# Python
from traceback import print_tb as print_traceback


# The decision authority serves as the central evaluator of authorization
#     requests and their bound attributes, and ultimately decides whether to
#     grant or deny them.
class DecisionAuthority:
    @classmethod
    def authorize(cls, request):
        # Make sure that the given request is correctly constructed.
        assert_subclass(request, AuthorizationRequest)
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
                print("Inapplicable policy: %s %s" % (type(error), error))
                print_traceback(error.__traceback__)
        
        # If we get to this point, then none of the policies evaluated to true.
        if all_inapplicable:
            # If every policy threw an error, then the authorization request is
            #     inapplicable.
            return AuthorizationResult.NOT_APPLICABLE
        else:
            # Otherwise, at least one policy evaluated to false.
            return AuthorizationResult.DENY