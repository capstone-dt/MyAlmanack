from ..decision import DecisionAuthority

# Django
from django.core.exceptions import PermissionDenied


class EnforcementAuthority:
    @classmethod
    def authorize(cls, request):
        return DecisionAuthority.authorize(request)
    
    @classmethod
    def is_permitted(cls, request):
        return DecisionAuthority.is_permitted(request)
    
    @classmethod
    def authorize_http(cls, http_request, action, resource, redirect_403=True):
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