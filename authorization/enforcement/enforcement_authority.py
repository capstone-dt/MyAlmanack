from ..utilities.reflection import assert_subclass

# Django
from django.core.exceptions import PermissionDenied
from django.http.request import HttpRequest


# The enforcement authority exposes the available authorization enforcement
#     methods to the API users of the subsystem and serves as an intermediary
#     between the users and the decision authority.
class EnforcementAuthority:
    # This calls the decision authority to authorize an authorization request.
    @classmethod
    def authorize(cls, request):
        from ..decision.decision_authority import DecisionAuthority
        return DecisionAuthority.authorize(request)
    
    # This provides a simplified authorization method for use in Django views.
    # Since Django view functions receive a request parameter with the active
    #     user bound to it, this method simply extracts the request's user and
    #     sets it as the subject of the authorization request.
    # This also encapsulates the return value of the authorization request and
    #     spits out a boolean value for simplified API usage.
    @classmethod
    def authorize_http(
        cls,
        http_request,
        action,
        resource,
        context=None,
        redirect_403=False
    ):
        # Make sure http_request is a subclass of Django's HttpRequest class.
        assert_subclass(http_request, HttpRequest)
        
        # Create the authorization request.
        from .authorization_request import AuthorizationRequest
        authorization_request = AuthorizationRequest(
            subject=http_request.user,
            action=action,
            resource=resource,
            context=context if context is not None else http_request
        )
        
        # This is ordered this way because the permitted attribute is actually a
        #     function call using the @property decorator underneath. We want to
        #     call it (by referencing it) only once.
        if authorization_request.permitted:
            # If the authorization request is permitted, return True.
            return True
        else:
            # If the authorization request is denied, raise 403 or return False.
            if redirect_403:
                raise PermissionDenied
            else:
                return False