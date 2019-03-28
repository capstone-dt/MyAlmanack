from ..decorators import login_notrequired
from ..firebase import invalidate_session
from ..utils import redirect_next

# Django
from django.contrib.auth import logout as _logout


@login_notrequired
def logout(request):
	if request.user.is_authenticated:
		invalidate_session(request)
		_logout(request)
	return redirect_next(request)