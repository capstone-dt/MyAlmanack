# Expose the enforcement authority.
# from .enforcement import EnforcementAuthority as PermissionEnforcementAuthority

# Expose authorization components.
from .decision import AuthorizationResult# as PermissionAuthorizationResult
from .decision import AuthorizationRequest# as PermissionAuthorizationRequest

# Expose action attributes.
from .attributes import actions