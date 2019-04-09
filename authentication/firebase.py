from .constants import SESSION_COOKIE, SESSION_COOKIE_LASTCHECKED

# Django
from django.conf import settings

# Firebase
import firebase_admin
from firebase_admin import auth as FirebaseAuth

# Python
from datetime import timedelta
from time import time


# Initialize the core Firebase admin application.
Firebase = firebase_admin.initialize_app(
	firebase_admin.credentials.Certificate(
		"configs/authentication/firebase_admin_sdk_key.json"
	)
)


def get_session_claims(request, check_revoked=False):
	session_cookie = request.session[SESSION_COOKIE]
	return FirebaseAuth.verify_session_cookie(session_cookie, check_revoked)


def is_session_valid(request):
	try:
		last_checked = request.session[SESSION_COOKIE_LASTCHECKED]
		
		# Check for session revocation if a certain amount of time has passed.
		check_revoked = time() - last_checked >= 5 * 60
		
		# If this succeeds, then the Firebase session is valid.
		get_session_claims(request, check_revoked)
		
		# Update the last checked timestamp.
		request.session[SESSION_COOKIE_LASTCHECKED] = time()
		return True
	except:
		return False


def validate_session(request, id_token):
	expires_in = timedelta(seconds=settings.SESSION_COOKIE_AGE)
	session_cookie = FirebaseAuth.create_session_cookie(id_token, expires_in)
	request.session[SESSION_COOKIE] = session_cookie
	request.session[SESSION_COOKIE_LASTCHECKED] = time()


def invalidate_session(request):
	try:
		FirebaseAuth.revoke_refresh_tokens(get_session_claims(request)["sub"])
	finally:
		request.session.pop(SESSION_COOKIE, None)
		request.session.pop(SESSION_COOKIE_LASTCHECKED, None)