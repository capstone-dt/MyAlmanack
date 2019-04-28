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
firebase_admin.initialize_app(firebase_admin.credentials.Certificate(
	"configs/authentication/firebase_admin_sdk_key.json"
))


# This returns the Firebase session claims attached to a Django request.
def get_session_claims(request, check_revoked=False):
	session_cookie = request.session[SESSION_COOKIE]
	return FirebaseAuth.verify_session_cookie(session_cookie, check_revoked)


# This checks whether the Firebase session attached to a Django request is
#     valid.
def is_session_valid(request):
	try:
	    # Extract the time that the session was last checked.
		last_checked = request.session[SESSION_COOKIE_LASTCHECKED]
		
		# Check for session revocation if a certain amount of time has passed.
		check_revoked = time() - last_checked >= 5 * 60 # 5 minutes
		
		# If this succeeds, then the Firebase session is valid.
		get_session_claims(request, check_revoked)
		
		# Update the last checked timestamp.
		request.session[SESSION_COOKIE_LASTCHECKED] = time()
		return True
	except:
		return False


# This validates a Django request's session with a given Firebase ID token.
def validate_session(request, id_token):
    # Calculate the session cookie expiration time relative to now.
	expires_in = timedelta(seconds=settings.SESSION_COOKIE_AGE)
	
	# Create a session cookie using the ID token.
	session_cookie = FirebaseAuth.create_session_cookie(id_token, expires_in)
	
	# Set the session cookies.
	request.session[SESSION_COOKIE] = session_cookie
	request.session[SESSION_COOKIE_LASTCHECKED] = time()


# This invalidates the Firebase session attached to a Django request.
def invalidate_session(request):
	try:
		FirebaseAuth.revoke_refresh_tokens(get_session_claims(request)["sub"])
	finally:
	    # Remove the session cookies.
		request.session.pop(SESSION_COOKIE, None)
		request.session.pop(SESSION_COOKIE_LASTCHECKED, None)