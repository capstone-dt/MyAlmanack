import authorization.api
from authentication.firebase import get_session_claims

# Django
from django.contrib.auth import get_user_model
from django.http import Http404
from django.shortcuts import render


def profile(request, uid):
    # Get the user from their Firebase ID given in the URL.
    try:
        user = get_user_model().objects.get(username=uid)
    except get_user_model().DoesNotExist:
        raise Http404
    
    # Check authorization.
    authorization.api.authorize(
        request,
        action=authorization.api.actions.user.profile.ViewUserProfile,
        resource=user
    )
    
    # Render the profile page.
    claims = get_session_claims(request)
    return render(request, "authorization/profile.html", context={
        "name": claims["name"],
        "image": claims["picture"],
        "claims": claims
    })