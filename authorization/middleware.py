from .enforcement import EnforcementAuthority


class AuthorizationMiddleware:
    def __init__(self, get_response):
        self.get_response = get_response
    
    def __call__(self, request):
        # Process request?
        return self.get_response(request)
    
    def process_view(self, request, view, *view_args, **view_kwargs):
        if hasattr(view, "_authorization_action"):
            # If the view has defined an action, check its authorization.
            EnforcementAuthority.authorize_http(
                http_request=request,
                action=view._authorization_action,
                resource=view._authorization_resource,
                redirect_403=True
            )