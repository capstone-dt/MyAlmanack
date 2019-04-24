from . import views

# Django
from django.urls import path


urlpatterns = [
	path("", views.index, name="index"),
	path("profile/<slug:uid>", views.profile, name="profile"),
	path("test", views.test, name="test"),
]