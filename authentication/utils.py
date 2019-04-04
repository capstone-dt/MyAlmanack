from django.conf import settings
from django.shortcuts import redirect


def redirect_login(request):
	return redirect((
		settings.LOGIN_URL + "?next=" + request.GET.get("next", request.path)
	) if request.path != settings.LOGIN_URL else settings.LOGIN_URL)


def redirect_next(request):
	return redirect(request.GET.get("next", settings.LOGIN_REDIRECT_URL))