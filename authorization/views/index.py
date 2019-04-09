from authorization import AuthorizationRequest, actions

# Django
from django.shortcuts import render
from django.utils.html import escape


def index(request):
    authorization_request = AuthorizationRequest(
        subject=request.user,
        action=actions.user.profile.ViewProfile,
        resource=request.user,
        context=request
    )
    
    return render(request, "authorization/index.html", context={
        "message": escape(
            "%s -> %s" %
            (authorization_request, authorization_request.authorize())
        )
    })