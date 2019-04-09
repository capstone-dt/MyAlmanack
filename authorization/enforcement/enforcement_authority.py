from ..decision import DecisionAuthority
from ..utilities._class import assert_subclass

# Django
from django.core.exceptions import PermissionDenied
from django.http.request import HttpRequest


class EnforcementAuthority:
    @classmethod
    def authorize(cls, request):
        return DecisionAuthority.authorize(request)
    
    @classmethod
    def is_permitted(cls, request):
        return DecisionAuthority.is_permitted(request)
    
    @classmethod
    def authorize_http(cls, http_request, action, resource, redirect_403=True):
        # Make sure http_request is a subclass of Django's HttpRequest class.
        assert_subclass(http_request, HttpRequest)
        
        # Create the authorization request.
        from .authorization_request import AuthorizationRequest
        request = AuthorizationRequest(
            subject=http_request.user,
            action=action,
            resource=resource,
            context=http_request
        )
        
        if cls.is_permitted(request):
            return True
        else:
            if redirect_403:
                raise PermissionDenied
            else:
                return False