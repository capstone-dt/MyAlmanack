from .authorization_result import AuthorizationResult


class DecisionAuthority:
    @classmethod
    def authorize(cls, request):
        result = request.action.authorize(request)
        
        # Make sure that the authorization result is one of enumeration values.
        if not isinstance(result, AuthorizationResult):
            raise ValueError(
                "The authorization request returned an invalid result: %s" %
                result
            )
        
        return result
    
    @classmethod
    def is_permitted(cls, request):
        return cls.authorize(request) == AuthorizationResult.PERMIT