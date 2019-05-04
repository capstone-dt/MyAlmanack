from .attributes import Action, Resource
from .utilities.reflection import assert_subclass


# This binds an authorization's action and resource attributes to a Django view
#     function, which gets checked before the view function is called.
# This is therefore unsuitable for use cases where the resource attribute is
#     retrieved during the view function's runtime.
def permission_required(action, resource):
    # Make sure that the given action and resource are of correct subclasses.
    assert_subclass(action, Action)
    assert_subclass(resource, Resource)
    
    # Python decorator handling:
    # @decorator(arg) def func(): ... --> decorator(arg)(func)
    def decorator(view_function):
        setattr(view_function, "_authorization_action", action)
        setattr(view_function, "_authorization_resource", resource)
        return view_function
    
    # Return the modified decorator.
    return decorator