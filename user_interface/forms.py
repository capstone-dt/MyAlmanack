from django import forms


class EventForm(forms.Form):
	post = forms.CharField()
