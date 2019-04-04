from .firebase import is_session_valid
from .utils import redirect_login

# Django
from django.conf import settings
from django.shortcuts import redirect


class FirebaseSessionMiddleware:
	def __init__(self, get_response):
		self.get_response = get_response
	
	def __call__(self, request):
		return self.get_response(request)
	
	def process_view(self, request, view, *view_args, **view_kwargs):
		# Check if the view requires authentication.
		login_required = not getattr(
		    view,
		    "_authentication_login_notrequired",
		    False
		)
		
		# Force re-login if the view requires authentication and the user is not
		#     logged in or the session is invalid.
		if login_required and (
			not request.user.is_authenticated or not is_session_valid(request)
		):
			return redirect_login(request)