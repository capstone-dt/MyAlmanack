"""WEBSITECORE URL Configuration

"""
from django.urls import path, re_path

from . import views

app_name = "WEBSITECORE"

urlpatterns = [
	path("", views.ProfileView.as_view(), name="profile"),
	path("profile", views.nullAlias, name="profile"),
	path("profile/", views.nullAlias, name="profile"),
	re_path(r'^profile/(?P<alias>[A-Za-z0-9]+)/$', views.ProfileView.as_view(), 
		name="profile"),
	path("profile/edit", views.EditProfileView.as_view(), name="editProfile"),
	re_path(r'^group/(?P<group_name>[A-Za-z0-9]+)/$', views.GroupView.as_view(), 
		name="group"),
	path("default", views.DefaultView.as_view(), name="default"),
	path("default/", views.DefaultView.as_view(), name="default"),
	path("search", views.SearchView.as_view(), name="search"),
	path("search/", views.SearchView.as_view(), name="search"),
]
