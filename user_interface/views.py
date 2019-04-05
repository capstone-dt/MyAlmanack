from django.views.generic import TemplateView
from django.shortcuts import render
from django.http import HttpResponse
from user_interface.forms import EventForm
from user_interface.forms import EditProfileForm
from user_interface.forms import SearchForm
import base64
import os
import json

def getDummyData(dummy_file):
	dummy_dir = "/user_interface/static/dummy_data/"
	extension = ".txt"
	cwd = os.getcwd()
	path = cwd + dummy_dir + dummy_file + extension
	data = open(path, "r").readlines()
	grid = []
	for line in data:
		curr = line.split("\t")
		for i in range(0,len(curr)):
			curr[i] = curr[i].replace("\n", "")
			curr[i] = curr[i].replace("\"", "")
		if len(curr[0]) == 0:
			continue
		grid.append(curr)
	headers = grid[0]
	structs = []
	for i in range(1, len(grid)):
		curr_struct = {}
		for j in range(0, len(grid[i])):
			curr_struct[headers[j]] = grid[i][j]
		structs.append(curr_struct)
	return structs

def getProfilePictureBase64(file_name):
	picture_dir = "/user_interface/static/profile_pictures/"
	extension = ".png"
	cwd = os.getcwd()
	file_loc = cwd + picture_dir + file_name + extension
	encoded_string = ""
	with open(file_loc, "rb") as image_file:
		encoded_string = base64.b64encode(image_file.read())
	retval = encoded_string.decode('utf-8')
	return retval

def getCurrUser(profile_json, firebase_id):
	for user in profile_json:
		# print(user)
		if user["firebase_id"] == firebase_id:
			return [user]
	return [{}]

class ProfileView(TemplateView):
	template_name = 'user_interface/profile.html'

	def dummy(self, event_form, request):
		search_form = SearchForm()
		eventstructs = getDummyData("event_table")
		eventjson = str(json.dumps(eventstructs))
		profilestructs = getDummyData("profile_table")
		profilejson = str(json.dumps(profilestructs))
		contactstructs = getDummyData("contact_list_table")
		contactjson = str(json.dumps(contactstructs))
		currentuserjson = str(json.dumps(getCurrUser(profilestructs, "88")))
		response = render(
			request=request,
			template_name=self.template_name,
			context={
				"event_form" : event_form,
				"search_form" : search_form, 
				"dummy_events" : eventjson, 
				"dummy_profiles" : profilejson,
				"dummy_contacts" : contactjson,
				"user" : str(currentuserjson),
				"calendarFrame" : "sub_templates/calendarFrame.html"
			}
		)
		return response

	def get(self, request):
		event_form = EventForm()
		return self.dummy(event_form, request)

	def post(self, request):
		print("POST REQUESTED")
		switchType = request.POST.get('formType')
		print(request.POST.get('formType'))
		event_form = EventForm()
		if(switchType == "SubmitEvent"):
			event_form = EventForm(request.POST)
			print(event_form)
			return self.dummy(event_form, request)
		elif(switchType == "FriendRequest"):
			event_form = EventForm(request.POST)
			print(event_form)
			return self.dummy(event_form, request)

class EditProfileView(TemplateView):
	template_name = 'user_interface/edit_profile.html'

	def get(self, request):
		edit_form = EditProfileForm()
		search_form = SearchForm()
		response = render(
			request=request,
			template_name=self.template_name,
			context={"edit_form" : edit_form, "search_form" : search_form}
		)
		return response

	def post(self, request):
		edit_form = EditProfileForm(request.POST)
		search_form = SearchForm()
		response = render(
			request=request,
			template_name=self.template_name,
			context={"edit_form" : edit_form, "search_form" : search_form}
		)
		return response

class GroupView(TemplateView):
	template_name = 'user_interface/group.html'

	def get(self, request):
		search_form = SearchForm()
		return render(
			request=request,
			template_name=self.template_name,
			context={"search_form" : search_form}
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
		search_form = SearchForm()
		return render(
			request=request,
			template_name=self.template_name,
			context={"search_form" : search_form}
		)

	def post(self, request):
		search_form = SearchForm(request.POST)
		print(search_form)
		return render(
			request=request,
			template_name=self.template_name,
			context={"search_form" : search_form}
		)

