import authorization

# Django
from django.shortcuts import render
from django.utils.html import escape


def index(request):
    authorization_request = authorization.AuthorizationRequest(
        subject=request.user,
        action=authorization.actions.user.profile.EditProfile,
        resource=request.user,
        context=request
    )
    
    return render(request, "authorization/index.html", context={
        "message": escape(
            "%s -> %s" %
            (authorization_request, authorization_request.authorize())
        )
    })