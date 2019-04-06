from django import forms
from django.contrib.postgres.forms import SimpleArrayField


class EventForm(forms.Form):
	EIname = forms.CharField(widget=forms.HiddenInput())
	EIstart = forms.DateField(widget=forms.HiddenInput())
	EIend = forms.DateField(widget=forms.HiddenInput())
	EIrepeat = forms.CharField(widget=forms.HiddenInput())
	EIrepeat_pattern = forms.CharField(widget=forms.HiddenInput())
	EIuntil = forms.DateField(widget=forms.HiddenInput())
	# Split manually
	EIinvite = forms.CharField(widget=forms.HiddenInput())
	EIwhitelist = forms.CharField(widget=forms.HiddenInput())
	EIblacklist = forms.CharField(widget=forms.HiddenInput())

class EditProfileForm(forms.Form):
	PIfirst = forms.CharField(widget=forms.HiddenInput())
	PIlast = forms.CharField(widget=forms.HiddenInput())
	PIemail = forms.CharField(widget=forms.HiddenInput())
	PIbirthday = forms.DateField(widget=forms.HiddenInput())
	PIphone = forms.CharField(widget=forms.HiddenInput())
	PIorganization = forms.CharField(widget=forms.HiddenInput())
	PIdescription = forms.CharField(widget=forms.HiddenInput())

class FriendRequestForm(forms.Form):
	FIalias = forms.CharField(widget=forms.HiddenInput())

class SearchForm(forms.Form):
	SIstring = forms.CharField(widget=forms.HiddenInput())