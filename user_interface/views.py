from django.views.generic import TemplateView
from django.shortcuts import render
from django.http import HttpResponse
from user_interface.forms import EventForm
from user_interface.forms import EditProfileForm
import base64
import os

def getProfilePictureBase64(file_name):
	picture_dir = "\\user_interface\\static\\profile_pictures\\"
	extension = ".png"
	cwd = os.getcwd()
	file_loc = cwd + picture_dir + file_name + extension
	encoded_string = ""
	with open(file_loc, "rb") as image_file:
		encoded_string = base64.b64encode(image_file.read())
	retval = encoded_string.decode('utf-8')
	return retval

class ProfileView(TemplateView):
	template_name = 'user_interface/profile.html'

	def get(self, request):
		event_form = EventForm()
		response = render(
			request=request,
			template_name=self.template_name,
			context={"event_form" : event_form}
		)
		return response

	def post(self, request):
		event_form = EventForm(request.POST)
		print("POST REQUESTED")
		print(event_form)
		response = render(
			request=request,
			template_name=self.template_name,
			context={"event_form" : event_form}
		)
		return response

class EditProfileView(TemplateView):
	template_name = 'user_interface/edit_profile.html'

	def get(self, request):
		edit_form = EditProfileForm()
		response = render(
			request=request,
			template_name=self.template_name,
			context={"edit_form" : edit_form}
		)
		return response

	def post(self, request):
		edit_form = EditProfileForm(request.POST)
		response = render(
			request=request,
			template_name=self.template_name,
			context={"edit_form" : edit_form}
		)
		return response

class GroupView(TemplateView):
	template_name = 'user_interface/group.html'

	def get(self, request):
		return render(
			request=request,
			template_name=self.template_name,
			context={}
		)

class DefaultView(TemplateView):
	template_name = 'user_interface/default.html'

	def get(self, request):
		return render(
			request=request,
			template_name=self.template_name,
			context={}
		)

class SearchView(TemplateView):
	template_name = 'user_interface/search.html'

	def get(self, request):
		return render(
			request=request,
			template_name=self.template_name,
			context={}
		)

