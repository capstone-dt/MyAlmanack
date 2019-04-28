from .firebase import get_session_claims

# Django
from django.contrib.auth import get_user_model
from django.contrib.auth.backends import ModelBackend
User = get_user_model()


# The Firebase authentication backend is intended to override the default
#     Django model backend to modify Django's authentication behavior.
# Currently, it sets the Firebase UID to Django's default User model's username.
# This is because we chose to not override the default User model and decided to
#     create the Profile model instead based on Justin's database design.
class FirebaseAuthenticationBackend(ModelBackend):
    # This overrides Django's authentication behavior to take in an HttpRequest
    #     object with the Firebase session claims attached to it instead.
	def authenticate(self, request):
		try:
			claims = get_session_claims(request, check_revoked=True)
		except:
			# The session is invalid. Force the user to login.
			return None
		
		try:
			# Return the user if they already exist.
			user = User.objects.get(username=claims["uid"])
		except User.DoesNotExist:
			# If the user does not already exist, create them.
			user = User(username=claims["uid"])
			user.save()
		return user
	
	# This is just boilerplate Django model backend stuff.
	def get_user(self, id):
		try:
			return User.objects.get(pk=id)
		except User.DoesNotExist:
			return None