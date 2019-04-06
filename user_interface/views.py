from django.views.generic import TemplateView
from django.shortcuts import render
from django.http import HttpResponse
from django.contrib.auth.models import User
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

def filterDummyEventsAlias(eventstructs, alias):
	ret_events = []
	for temp_event in eventstructs:
		if temp_event["event_creator_alias"] == alias:
			ret_events.append(temp_event)
	return ret_events

def filterDummyContactsAlias(contactstructs, contact_list_id):
	for temp_contact in contactstructs:
		if temp_contact["contact_list_id"] == contact_list_id:
			return temp_contact
	return None

def genHiddenEvent(passed_event):
	hiddenstruct = {}
	hiddenstruct["event_id"] = "-1"
	hiddenstruct["description"] = "Hidden"
	hiddenstruct["participating_users"] = ""
	hiddenstruct["event_admins"] = ""
	hiddenstruct["whitelist"] = ""
	hiddenstruct["blacklist"] = ""
	hiddenstruct["start_date"] = passed_event["start_date"]
	hiddenstruct["end_date"] = passed_event["end_date"]
	hiddenstruct["event_creator_alias"] = passed_event["event_creator_alias"]
	hiddenstruct["event_creator_firebase_id"] = passed_event["event_creator_firebase_id"]
	hiddenstruct["isHidden"] = "true"
	return hiddenstruct


def filterAccessFriendEvents(friend_events, user_alias):
	print("FILTER FRIEND EVENTS", user_alias)
	ret_filtered = []
	for temp_event in friend_events:
		whitelist_str = temp_event["whitelist"].replace(" ", "")
		blacklist_str = temp_event["blacklist"].replace(" ", "")
		whitelist = whitelist_str.split(",");
		blacklist = blacklist_str.split(",");
		whitelist_empty = False
		blacklist_empty = False
		if len(whitelist_str) == 0:
			whitelist_empty = True
		if len(blacklist_str) == 0:
			blacklist_empty = True
		if whitelist_empty and blacklist_empty == False:
			isblacklisted = False
			for blacklisted in blacklist:
				if blacklisted == user_alias:
					isblacklisted = True
					break
			if isblacklisted:
				hiddenstruct = genHiddenEvent(temp_event)
				ret_filtered.append(hiddenstruct)
				continue
		if whitelist_empty == False and blacklist_empty:
			iswhitelisted = False
			for whitelisted in whitelist:
				if whitelisted == user_alias:
					iswhitelisted = True
					break
			if iswhitelisted == False:
				hiddenstruct = genHiddenEvent(temp_event)
				ret_filtered.append(hiddenstruct)
				continue
		if whitelist_empty == False and blacklist_empty == False:
			continue
		ret_filtered.append(temp_event)
	return ret_filtered


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
		user_firebase_id = "88"
		currentuserstruct = getCurrUser(profilestructs, user_firebase_id)
		currentuserjson = str(json.dumps(currentuserstruct))
		# print(currentuserstruct)
		user_alias = currentuserstruct[0]["alias"]
		user_events = filterDummyEventsAlias(eventstructs, user_alias)
		user_contact_list_id = currentuserstruct[0]["contact_list_id"]
		user_contact_list = filterDummyContactsAlias(contactstructs, user_contact_list_id)
		friend_names = user_contact_list["contact_names"].replace(" ", "").split(",")
		print(friend_names)
		friend_events = []
		for friend_alias in friend_names:
			curr_events = filterDummyEventsAlias(eventstructs, friend_alias)
			for temp_event in curr_events:
				friend_events.append(temp_event)
		filtered_friend_events = filterAccessFriendEvents(friend_events, user_alias)

		user_events_json = str(json.dumps(user_events))
		filtered_friend_events_json = str(json.dumps(filtered_friend_events))
		user_contact_list_json = str(json.dumps(user_contact_list))

		def_prof_pic = getProfilePictureBase64("default_profile");
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
				"user_events" : user_events_json,
				"friend_events" : filtered_friend_events_json,
				"user_contact_list" : user_contact_list_json,
				"calendarFrame" : "sub_templates/calendarFrame.html",
				"default_profile" : def_prof_pic
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
		#form.data['field_name']
		search_term = search_form.data['SIstring']
		events = searchEvents(search_term)
		friends = searchFriends(search_term)
		users = searchUsers(search_term)
		groups = searchGroups(search_term)
		return render(
			request=request,
			template_name=self.template_name,
			context={"search_form" : search_form,
				"events" : events,
				"friends" : friends,
				"users" : users,
				"groups" : groups
			}
		)

def aliasToFirebaseId(alias):
	firebase_id = ""
	# query database
	return firebase_id

def firebaseIdToAlias(firebase_id):
	alias = ""
	# query database
	return alias


# FRIEND REQUESTS
# insert outgoing / incoming
def sendFriendRequest(send_alias, recieve_alias):
	return None

# remove outgoing / incoming
def actionFriendRequest(send_alias, recieve_alias, action):
	temp = ""
	if(action):
		#insert to contact list aliases for both people
		temp = "temp"
	# remove
	return None

# EVENT INVITES
# insert
def sendEventInvite(send_alias, recieve_alias, event_id):
	return None

#remove
def actionEventInvite(send_alias, recieve_alias, action, event_id):
	temp = ""
	if(action):
		# add to recipient only
		temp = "temp"
	# remove
	return None

# GROUP INVITES
# add outgoing incoming
def sendGroupInvite(send_name, recieve_name, direction):
	# add to incoming of all group admins
	# send_name --> recieve_name
	temp = ""
	if(direction=="g_u"):
		# group_name = send_name
		# recieve_alias = recieve_name
		temp = ""
	elif(direction=="u_g"):
		# send_alias = send_name
		# recieve_group_name = recieve_name
		temp = ""
	return None

def actionGroupInvite(send_alias, recieve_alias, action, direction):
	temp = ""
	group_name = ""
	user_alias = ""
	if(direction=="g_u"):
		# group_name = send_name
		# recieve_alias = recieve_name
		# remove requests from both group outgoing & user incoming
		temp = ""
	elif(direction=="u_g"):
		# send_alias = send_name
		# recieve_group_name = recieve_name
		# remove requests from both user outgoing & group incoming
		temp = ""
	if(action):
		temp = ""
		#add user to group
		#refs group_name, user_alias
	return None

# USER DATA

def getUserData_firebase_id(firebase_id):
	return None

def getUserData_alias(alias):
	return None

def editUserData(alias, phone_num, last_name, first_name,
	email, contact_list, organization, user_desc, user_events):
	return None


def getFriendsUserData_alias(alias):
	return None

def getFriendsUserData_firebase_id(firebase_id):
	return None

# CONTACT LIST

def getContactListData_alias(alias):
	return None

def getContactListData_firebase_id(firebase_id):
	return None

# EVENTS
# Get the participating event ids (user data) 
# and query the event table by id
def getUserEvents_alias(alias):
	return None

def getUserEvents_firebase_id(firebase_id):
	return None

# call the send event invite method
# invites : everyone who's invited (aliases)
def createEvent(event_id, description, invites, 
	event_admins, whitelist, blacklist, start_date,
	end_date, event_creator_firebase_id):
	return None

def createRepeatEvent(event_id, description, invites, 
	event_admins, whitelist, blacklist, start_date,
	end_date, event_creator_firebase_id, 
	# Repeat params:
	rep_event_id, rep_type, start_time, end_time, week_arr):

	return None

def editEvent(event_id, description, event_admins, whitelist, 
	blacklist, start_date, end_date):
	return None


# FILTER BASED ON WHITELIST AND BLACKLIST
# if can't view return dummy event with constant event id
def getFriendEvents_alias(alias):
	return None

def getFriendEvents_firebase_id(firebase_id):
	return None

# SIMILARITY (search page) 
# Returns query-set (generated by django)
# Trigram Similarity
# filter based on similarity
def searchEvents(search_term):
	print("events", search_term)
	return None

def searchFriends(search_term):
	print("friends", search_term)
	return None

def searchUsers(search_term):
	print("users", search_term)
	return None

def searchGroups(search_term):
	print("groups", search_term)
	return None

