from .attribute import Attribute


# The Subject class simply provides an interface for AuthorizationRequest's
#     subject attribute by wrapping specific classes of objects passed in by the
#     subsystem's API users.
class Subject(Attribute):
    pass