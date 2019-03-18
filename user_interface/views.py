from django.shortcuts import render
from django.http import HttpResponse

# In myalmanack folder
# In main/views.py in sentdex tutorial
# Create your views here.
def homepage(request):
	return render(
		# Pass the request
		request=request,
		# Where to find template
		template_name="user_interface/register.html",
		# Pass in variable 'people' using Person.objects.all
		context={}
	)

def editProfile(request):
	return render(
		# Pass the request
		request=request,
		# Where to find template
		template_name="user_interface/edit_profile.html",
		# Pass in variable 'people' using Person.objects.all
		context={}
	)

def profile(request):
	return render(
		# Pass the request
		request=request,
		# Where to find template
		template_name="user_interface/profile.html",
		# Pass in variable 'people' using Person.objects.all
		context={}
	)

def register(request):
	return render(
	request = request,
	template_name = "user_interface/register.html",
	context={}
	)

def login(request):
	return render(
	request = request,
	template_name = "user_interface/login.html",
	context={}
	)

def search(request):
	return render(
	request = request,
	template_name = "user_interface/search.html",
	context={}
	)

def calendarTest(request):
	return render(
	request =request,
	template_name = "user_interface/calendarTest.html",
	context={}
	)
