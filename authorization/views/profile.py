from authorization import authorize, actions

# Django
from django.http import HttpResponse


def profile(request):
    # Do some processing to find the user.
    from django.contrib.auth import get_user_model
    user = get_user_model().objects.get(username=request.user.username)
    
    # Authorize the request. This will automatically redirect to 403 if denied.
    authorize(request, actions.user.profile.ViewProfile, user)
    
    # Perform stuff.
    return HttpResponse(
        "Congratulations, you have permission to view this profile!"
    )