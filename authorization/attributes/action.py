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
                if policy.evaluate(request):
                    return AuthorizationResult.PERMIT
                else:
                    return AuthorizationResult.DENY
            except Exception as error:
                print("Skipping inapplicable action authorization:", error)
        
        # If we get to this point, then none of the policies were applicable.
        return AuthorizationResult.NOT_APPLICABLE