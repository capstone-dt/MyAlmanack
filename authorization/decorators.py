from .attributes import Action
from .utils import assert_subclass


def permission_required(action):
    assert_subclass(action, Action)
    def decorator(view_function):
        setattr(view_function, "_authorization_action", action)
        return view_function
    return decorator