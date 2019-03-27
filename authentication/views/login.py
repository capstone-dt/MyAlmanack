from ..decorators import login_notrequired
from ..firebase import FirebaseAuth, validate_session
from ..utils import redirect_login, redirect_next

# Django
from django.conf import settings
from django.contrib.auth import authenticate, login as _login
from django.shortcuts import redirect, render

# Python
from time import time


@login_notrequired
def login(request):
	# If the user is already logged in, redirect them back.
	if request.user.is_authenticated:
		return redirect_next(request)
	
	# Get the Firebase ID token from the POST request.
	id_token = request.POST.get("firebase_idtoken")
	
	# Show the login dialog if no ID token was given.
	if not id_token:
		return render(request, "authentication/login.html")
	
	# Force re-login if the ID token is invalid or has been revoked.
	try:
		claims = FirebaseAuth.verify_id_token(id_token, check_revoked=True)
	except:
		return redirect_login(request)
	
	# Force re-login for incomplete authentications over five minutes old.
	if time() - claims["auth_time"] >= 5 * 60:
		return redirect_login(request)
	
	# Validate the session with Firebase.
	validate_session(request, id_token)
	
	# Authenticate with Django and log the user in.
	user = authenticate(request)
	if user:
		_login(request, user)
		return redirect_next(request)
	else:
		# Force re-login if user authentication with Django failed.
		return redirect_login(request)