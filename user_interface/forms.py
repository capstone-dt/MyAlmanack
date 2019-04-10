from django import forms
from django.contrib.postgres.forms import SimpleArrayField


class EventForm(forms.Form):
	EIname = forms.CharField(widget=forms.HiddenInput())
	EIstart = forms.CharField(widget=forms.HiddenInput())
	EIend = forms.CharField(widget=forms.HiddenInput())
	# Split manually
	EIinvite = forms.CharField(widget=forms.HiddenInput())
	EIwhitelist = forms.CharField(widget=forms.HiddenInput())
	EIblacklist = forms.CharField(widget=forms.HiddenInput())
	EIrepeat = forms.CharField(widget=forms.HiddenInput(), required=False)
	EIrepeat_pattern = forms.CharField(widget=forms.HiddenInput(), required=False)

class GroupForm(forms.Form):
	GIname = forms.CharField(widget=forms.HiddenInput())
	GIdescription = forms.CharField(widget=forms.HiddenInput())
	GIinvite = forms.CharField(widget=forms.HiddenInput())

class EditProfileForm(forms.Form):
	PIfirst = forms.CharField(widget=forms.HiddenInput())
	PIlast = forms.CharField(widget=forms.HiddenInput())
	# ADDED
	PIalias = forms.CharField(widget=forms.HiddenInput())
	PIemail = forms.CharField(widget=forms.HiddenInput(), required=False)
	PIbirthday = forms.DateField(widget=forms.HiddenInput())
	PIphone = forms.CharField(widget=forms.HiddenInput(), required=False)
	PIorganization = forms.CharField(widget=forms.HiddenInput(), required=False)
	PIdescription = forms.CharField(widget=forms.HiddenInput(), required=False)

class FriendRequestForm(forms.Form):
	FIalias = forms.CharField(widget=forms.HiddenInput())

class FriendRemoveForm(forms.Form):
	FIalias = forms.CharField(widget=forms.HiddenInput())

class SearchForm(forms.Form):
	SIstring = forms.CharField(widget=forms.HiddenInput(), required=False)