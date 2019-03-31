from django.shortcuts import render
from django.http import HttpResponse
import numpy as np 
import cv2
import base64
import os
import json

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

def getProfilePictureBase64(file_name):
	picture_dir = "\\user_interface\\static\\profile_pictures\\"
	extension = ".png"
	label = file_name
	cwd = os.getcwd()
	file_loc = cwd + picture_dir + label + extension
	encoded_string = ""
	with open(file_loc, "rb") as image_file:
		encoded_string = base64.b64encode(image_file.read())
	retval = encoded_string.decode('utf-8')
	return retval

def profile(request):
	picture = getProfilePictureBase64("default_profile")
	response = render(
		request=request,
		template_name="user_interface/profile.html",
		context={'temp_image' : picture}
	)
	return response

def group(request):
	return render(
		# Pass the request
		request=request,
		# Where to find template
		template_name="user_interface/group.html",
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
