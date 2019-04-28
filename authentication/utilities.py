from django.conf import settings
from django.shortcuts import redirect


# This redirects a user to the login page with the current page set as the next
#     page to redirect to on login completion.
def redirect_login(request):
	return redirect((
		settings.LOGIN_URL + "?next=" + request.GET.get("next", request.path)
	) if request.path != settings.LOGIN_URL else settings.LOGIN_URL)


# This redirects a user to the page in the URL's "next" parameter.
def redirect_next(request):
	return redirect(request.GET.get("next", settings.LOGIN_REDIRECT_URL))