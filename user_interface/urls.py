"""WEBSITECORE URL Configuration

"""
from django.urls import path

from . import views

app_name = "WEBSITECORE"

urlpatterns = [
	path("", views.homepage, name="homepage"),
	path("profile/edit", views.editProfile, name="editProfile"),
	path("profile", views.profile, name="profile"),
	path("profile/", views.profile, name="profile"),
	path("group", views.group, name="group"),
	path("group/", views.group, name="group"),
	path("register", views.register, name="register"),
	path("register/", views.register, name="register"),
	path("login", views.login, name="login"),
	path("login/", views.login, name="login"),
	path("search", views.search, name="search"),
	path("search/", views.search, name="search"),
	path("calendar/tests", views.calendarTest, name="calendarTest")
]
