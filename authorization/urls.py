from . import views

# Django
from django.urls import path


urlpatterns = [
	path("", views.index, name="index"),
	path("profile", views.profile, name="profile"),
]