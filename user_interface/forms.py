from django import forms


class EventForm(forms.Form):
	EIname = forms.CharField(widget=forms.HiddenInput())
	EIstart = forms.DateField(widget=forms.HiddenInput())
	EIend = forms.DateField(widget=forms.HiddenInput())
	EIrepeat = forms.CharField(widget=forms.HiddenInput())
	EIuntil = forms.DateField(widget=forms.HiddenInput())
	EIinvite = forms.CharField(widget=forms.HiddenInput())
	EIwhitelist = forms.CharField(widget=forms.HiddenInput())
	EIblacklist = forms.CharField(widget=forms.HiddenInput())
