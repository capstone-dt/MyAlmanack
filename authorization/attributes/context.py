from .attribute import Attribute


# The Context class simply provides an interface for AuthorizationRequest's
#     context attribute by wrapping specific classes of objects passed in by the
#     subsystem's API users.
class Context(Attribute):
    pass