from enum import Enum


# The AuthorizationResult enumeration class provides a set of appropriate return
#     values for authorization request evaluations.
class AuthorizationResult(Enum):
    PERMIT = "PERMIT"
    DENY = "DENY"
    NOT_APPLICABLE = "NOT_APPLICABLE"