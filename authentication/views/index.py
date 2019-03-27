from ..decorators import login_notrequired

# Django
from django.shortcuts import redirect, render


@login_notrequired
def index(request):
	if request.user.is_authenticated:
		return redirect("logged_in")
	else:
		return render(request, "authentication/index.html")