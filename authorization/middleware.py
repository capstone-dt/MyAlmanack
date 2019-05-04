from .enforcement.enforcement_authority import EnforcementAuthority


# This is an optional middleware that allows binding authorization actions and
#     resources before runtime using the @permission_required() decorator.
# This is not really useful for dynamic permission checking since the actions
#     and resources need to be known beforehand.
class AuthorizationMiddleware:
    # This is just boilerplate stuff for Django.
    def __init__(self, get_response): self.get_response = get_response
    def __call__(self, request): return self.get_response(request)
    
    # This intercepts view requests before they are served.
    def process_view(self, request, view, *view_args, **view_kwargs):
        if hasattr(view, "_authorization_action"):
            # If the view has defined an action, check its authorization.
            EnforcementAuthority.authorize_http(
                http_request=request,
                action=view._authorization_action,
                resource=view._authorization_resource,
                redirect_403=True
            )