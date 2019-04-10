from .attributes import Action
from .enforcement import AuthorizationRequest
from .utilities.reflection import assert_subclass

# Django
from django.core.exceptions import PermissionDenied

# Python
from functools import partial


def permission_required(action):
    # Make sure that the given action is a subclass of Action.
    assert_subclass(action, Action)
    
    # Define a function to allow the view function to set the authorization
    #     resource at runtime.
    def authorize(request, resource):
        authorization_request = AuthorizationRequest(
            subject=request.user,
            action=action,
            resource=resource,
            context=request
        )
        
        # If the user is unauthorized to view the page, raise an exception.
        if not authorization_request.is_permitted:
            raise PermissionDenied
    
    # Python decorator handling:
    # @decorator(arg) def func(): ... --> decorator(arg)(func)
    def decorator(view_function):
        return partial(view_function, authorize=authorize)
    
    # Return the modified decorator.
    return decorator