import authorization.api

# Django
from django.shortcuts import render
from django.utils.html import escape


def index(request):
    # Construct an authorization request using the AuthorizationRequest class.
    authorization_request = authorization.api.AuthorizationRequest(
        subject=request.user,
        action=authorization.api.actions.user.profile.EditUserProfile,
        resource=request.user
    )
    
    return render(request, "authorization/index.html", context={
        "message": escape(
            "%s -> %s" %
            (authorization_request, authorization_request.authorize())
        )
    })