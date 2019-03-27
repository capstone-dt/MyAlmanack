from . import views

# Django
from django.urls import path


urlpatterns = [
	path("", views.index, name="index"),
	path("login", views.login, name="login"),
	path("logout", views.logout, name="logout"),
	path("logged_in", views.logged_in, name="logged_in"),
	path("secret", views.secret, name="secret"),
]