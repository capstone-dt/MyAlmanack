import authorization

# Django
from django.http import HttpResponse


def profile(request):
    authorization.authorize(
        request,
        action=authorization.actions.user.profile.ViewProfile,
        resource=request.user
    )
    
    return HttpResponse(
        "Congratulations, you have permission to view this profile!"
    )