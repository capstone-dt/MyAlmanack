from authorization import authorize_http, actions
#from authorization.information.user import User

# Django
from django.http import HttpResponse


def profile(request):
    # Do some processing to find another user.
    some_other_user = request.user
    
    # Authorize the request. This will automatically redirect to 403 if denied.
    authorize_http(request, actions.user.profile.ViewProfile, some_other_user)
    
    # Perform stuff.
    return HttpResponse(
        "Congratulations, you have permission to view this profile!"
    )