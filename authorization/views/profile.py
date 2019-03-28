from authorization import actions
from authorization.decorators import permission_required

# Django
from django.http import HttpResponse


@permission_required(actions.user.profile.ViewProfile)
def profile(request):
    return HttpResponse(
        "Congratulations, you have permission to view this profile!"
    )