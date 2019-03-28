from ..decision import AuthorizationResult


class Action:
    @classmethod
    def authorize(cls, request):
        print("Action:", cls)
        print("Policies:", cls.policies)
        
        # Evaluate all the policies of this action.
        for policy in cls.policies:
            print("Evaluating policy:", policy)
            try:
                if not policy.evaluate(request):
                    return AuthorizationResult.DENY
            except Exception as error:
                print("Inapplicable action authorization:", error)
                return AuthorizationResult.NOT_APPLICABLE
        
        # If we get to this point, every policy has authorized the action.
        return AuthorizationResult.PERMIT