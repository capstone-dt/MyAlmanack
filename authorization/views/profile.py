import authorization.api

# MyAlmanack database (Justin's subsystem)
from database.models import Profile

# Django
from django.http import Http404
from django.shortcuts import render


def profile(request, uid):
    # Try to get the profile if it exists.
    try:
        profile = Profile.objects.get(firebase_id=uid)
    except Profile.DoesNotExist:
        raise Http404
    
    # Check authorization using the short-hand HTTP request authorize() method.
    authorization.api.authorize(request,
        action=authorization.api.actions.user.profile.ViewUserProfile,
        resource=profile,
        redirect_403=True
    )
    # If the authorization request is denied, the user will be redirected to the
    #     403 forbidden page.
    
    # Render the profile page.
    return render(request, "authorization/profile.html", context={
        "name": "%s %s" % (profile.first_name, profile.last_name)
    })