# Expose authorization enforcement components.
from .enforcement import (
    EnforcementAuthority as AuthorizationEnforcer,
    AuthorizationRequest,
    AuthorizationResult
)

# Expose the short-hand HTTP request authorization function.
authorize = AuthorizationEnforcer.authorize_http

# Expose action attributes.
from .attributes import actions