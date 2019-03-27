from .firebase import get_session_claims

# Django
from django.contrib.auth import get_user_model
from django.contrib.auth.backends import ModelBackend


User = get_user_model()


class FirebaseAuthenticationBackend(ModelBackend):
	def authenticate(self, request):
		try:
			claims = get_session_claims(request, check_revoked=True)
		except:
			# The session is invalid. Force the user to login.
			return None
		
		try:
			# Return the user if they exist.
			user = User.objects.get(username=claims["uid"])
		except User.DoesNotExist:
			# If the user does not exist, create them.
			user = User(username=claims["uid"])
			user.save()
		return user
	
	def get_user(self, id):
		try:
			return User.objects.get(pk=id)
		except User.DoesNotExist:
			return None