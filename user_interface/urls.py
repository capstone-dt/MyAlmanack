"""WEBSITECORE URL Configuration

"""
from django.urls import path, re_path

from . import views

app_name = "WEBSITECORE"

urlpatterns = [
	path("", views.nullAlias, name="profile"),
	path('', views.nullAlias, name="profile"),
	path("profile", views.nullAlias, name="profile"),
	path("profile/", views.nullAlias, name="profile"),
	path("profile/edit", views.EditProfileView.as_view(), name="editProfile"),
	path("profile/edit/", views.EditProfileView.as_view(), name="editProfile"),
	re_path(r'^profile/(?P<alias>[A-Za-z0-9]+)/$', views.ProfileView.as_view(), 
		name="profile"),
	re_path(r'^redirfb/(?P<firebase_id_requested>[A-Za-z0-9]+)/$', 
		views.redirFirebase, name="redirFirebase"),
	path('group/', views.nullGroup, name="group"),
	re_path(r'^group/(?P<group_name>[A-Za-z0-9]+)/$', views.GroupView.as_view(), 
		name="group"),
	re_path(r'^redirgn/(?P<group_name_requested>[A-Za-z0-9]+)/$', 
		views.redirGroupname, name="redirGroupname"),
	path("ajax/validate_alias/", views.validate_alias, name="validate_alias"),
	path("ajax/validate_group_name/", views.validate_group_name, name="validate_group_name"),
	path("default", views.DefaultView.as_view(), name="default"),
	path("default/", views.DefaultView.as_view(), name="default"),
	path("search", views.SearchView.as_view(), name="search"),
	path("search/", views.SearchView.as_view(), name="search"),
]
