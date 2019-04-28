from .firebase import is_session_valid
from .utilities import redirect_login

# Django
from django.contrib.auth import logout


# The Firebase session middleware ensures that all Django views are served only
#     if a Django request's session has a valid Firebase session attached to it.
# Use the @login_notrequired decorator to allow views to be served without
#     requiring a Firebase session.
class FirebaseSessionMiddleware:
    # This is just boilerplate stuff for Django.
    def __init__(self, get_response): self.get_response = get_response
    def __call__(self, request): return self.get_response(request)
    
    # This intercepts view requests before they are served.
    def process_view(self, request, view, *view_args, **view_kwargs):
        # Check if the view requires authentication.
        login_required = not (
            getattr(view, "_authentication_login_notrequired", False)
        )
        
        # Force re-login if the view requires authentication and the user is not
        #     logged in or the session is invalid.
        if login_required and (
            not request.user.is_authenticated or not is_session_valid(request)
        ):
            logout(request)
            return redirect_login(request)