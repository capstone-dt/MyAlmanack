"""WEBSITECORE URL Configuration

"""
from django.urls import path

from . import views

app_name = "WEBSITECORE"

urlpatterns = [
	path("", views.ProfileView.as_view(), name="profile"),
	path("profile/edit", views.EditProfileView.as_view(), name="editProfile"),
	path("profile", views.ProfileView.as_view(), name="profile"),
	path("profile/", views.ProfileView.as_view(), name="profile"),
	path("group", views.GroupView.as_view(), name="group"),
	path("group/", views.GroupView.as_view(), name="group"),
	path("default", views.DefaultView.as_view(), name="default"),
	path("default/", views.DefaultView.as_view(), name="default"),
	path("search", views.SearchView.as_view(), name="search"),
	path("search/", views.SearchView.as_view(), name="search"),
]
