from django.views.generic import TemplateView
from django.shortcuts import render
from django.http import HttpResponse
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
		response = render(
			request=request,
			template_name=self.template_name,
			context={}
		)
		return response

class EditProfileView(TemplateView):
	template_name = 'user_interface/edit_profile.html'

	def get(self, request):
		response = render(
			request=request,
			template_name=self.template_name,
			context={}
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

