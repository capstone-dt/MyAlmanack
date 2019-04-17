from django.views.generic import TemplateView
from django.shortcuts import render
from django.shortcuts import redirect
from django.http import HttpResponse
from django.http import HttpResponseRedirect
from django.contrib.auth.models import User
from database.views import *
from user_interface.forms import *
import base64
import os
import json
from authentication.firebase import get_session_claims
from django.contrib.auth import get_user_model
from django.contrib.auth.backends import ModelBackend

# - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - -#

# PROFILE PICTURE I/O

def getProfilePictureFirebaseId(firebase_id):
	try:
		file_loc = getProfilePictureLocation(firebase_id)
		fh = open(file_loc, 'r')
		return getProfilePictureBase64(firebase_id)
	except FileNotFoundError:
		return getProfilePictureBase64("default_profile")

def getProfilePictureLocation(file_name):
	picture_dir = "/user_interface/static/profile_pictures/"
	extension = ".png"
	cwd = os.getcwd()
	file_loc = cwd + picture_dir + file_name + extension
	return file_loc

def getProfilePictureBase64(file_name):
	file_loc = getProfilePictureLocation(file_name)
	encoded_string = ""
	with open(file_loc, "rb") as image_file:
		encoded_string = base64.b64encode(image_file.read())
	retval = encoded_string.decode('utf-8')
	return retval

def saveProfilePictueBase64(file_name, image_64_encode):
	file_loc = getProfilePictureLocation(file_name)
	if(image_64_encode == "$"):
		return
	split_string = image_64_encode.split(",")[1].encode('utf-8')
	image_64_decode = base64.decodestring(split_string)
	image_result = open(file_loc, 'wb')
	image_result.write(image_64_decode)

# - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - -#

# CALENDAR DATA

def getCalendarForms():
	retDict = {}
	retDict["event_form"] = EventForm()
	return retDict

def getCalendarDict(user_firebase_id, selected_id, mode):
	retDict = {
		"mode" : "",
		"calendar_data" : {
			"user_events" : [],
			"member_events" : [],
			"member_info" : [],
			"user_info" : {},
		},
	}
	retDict["mode"] = mode
	profile_data = getProfileData(user_firebase_id)
	retDict["calendar_data"]["user_info"] = profile_data
	user_events = []
	if(profile_data['user_events'] != None):
		user_events = getUserEvents(user_firebase_id)
	retDict["calendar_data"]["user_events"] = user_events
	if(mode == "USER"):
		data_contact_list = getContactListData(user_firebase_id)
		database_contact_ids = data_contact_list["contact_names"]
		if(database_contact_ids == None):
			database_contact_ids = []
		member_events = []
		member_info = []
		for f_id in database_contact_ids:
			curr_dict_f = {}
			curr_dict_f["firebase_id"] = f_id
			curr_dict_f["participating_events"] = []
			member_profile_data = getProfileData(f_id)
			curr_events_friend = []
			if(member_profile_data["user_events"] != None):
				curr_events_friend = getUserEvents(f_id)
			for ev in curr_events_friend:
				curr_dict_f["participating_events"].append(ev)
			member_events.append(curr_dict_f)
			member_info.append(member_profile_data)
		retDict["calendar_data"]["member_events"] = member_events
		retDict["calendar_data"]["member_info"] = member_info
	elif(mode == "FRIEND"):
		member_info = getProfileData(selected_id)
		member_events = []
		if(member_info["user_events"] != None):
			member_events = getUserEvents(selected_id)
		if(member_events == None):
			member_events = []
		retDict["calendar_data"]["member_events"] = member_events
		retDict["calendar_data"]["member_info"] = [getProfileData(selected_id)]
	elif(mode == "GROUP"):
		print("group selected")
		retDict["calendar_data"]["member_events"] = []
		retDict["calendar_data"]["member_info"] = []
	return retDict

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

# - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - -#

# HEADER

def getHeaderDict(firebase_id):
	retHeader = {
		"event_invites" : [],
		"friend_requests" : [],
		"group_requests" : {
			"join_requests" : [],
			"invites" : []
		}
	}
	user_firebase_id = firebase_id
	isValid = validFirebaseId(user_firebase_id);
	if(isValid == True):
		return retHeader

	contact_list = getContactListData(firebase_id)
	if(contact_list["received_event_invites"] == None):
		retHeader["event_invites"] = []
	else:
		event_invite_ids = contact_list["received_event_invites"]
		for e_id in event_invite_ids:
			curr_event_data = getEventData(e_id)
			retHeader["event_invites"].append(curr_event_data)
	if(contact_list["received_friend_requests"] == None):
		retHeader["friend_requests"] = []
	else:
		friend_invite_ids = contact_list["received_friend_requests"]
		print("recieved:", friend_invite_ids)
		for f_id in friend_invite_ids:
			request_data = getFriendRequestData(f_id)
			print("request_data", request_data)
			sender_id = request_data["sender_id"]
			curr_user = getProfileData(sender_id)
			curr_user["profile_picture"] = getProfilePictureFirebaseId(sender_id)
			curr_user["invite_id"] = f_id
			retHeader["friend_requests"].append(curr_user)
	if(contact_list["received_group_invites"] == None):
		retHeader["group_requests"]["invites"] = []
	else:
		group_invite_names = contact_list["received_group_invites"]
		for g_name in group_invite_names:
			curr_group_data = getGroupData(g_name)
			retHeader["group_requests"]["invites"].append(curr_group_data)
	return retHeader

def getHeaderForms():
	retDict = {
		"event_response" : EventRespondRequest(),
		"search_form" : SearchForm(),
		"friend_response" : FriendRespondRequest(),
		"group_response" : GroupRespondRequest(),
		"group_form" : GroupForm(),
	}
	return retDict

# - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - -#

# 404 View

def redir404(request):
	user_firebase_id = getCurrentFirebaseId(request)
	return render(
		request=request,
		template_name='user_interface/404.html',
		context={"user_header_database" : str(json.dumps(getHeaderDict(user_firebase_id))),
			"header_forms" : getHeaderForms(),}
	)

# - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - -#

# PROFILE

def getProfileForms():
	retDict = {}
	retDict["friend_req"] = FriendRequestForm();
	retDict["friend_rem"] = FriendRemoveForm();
	return retDict



def nullAlias(request):
	p = ProfileView()
	if(request.method == "POST"):
		return p.post(request, "")
	return p.get(request, "")

class ProfileView(TemplateView):
	template_name = 'user_interface/profile.html'

	def dummy(self, request, alias_requested):

		user_firebase_id = getCurrentFirebaseId(request)
		isValid = validFirebaseId(user_firebase_id);
		print("isvalid_id", isValid)

		if(isValid == True):
			return redirForce(request)

		profile_data = getProfileData(user_firebase_id)
		profile_data["profile_picture"] = getProfilePictureFirebaseId(user_firebase_id)
		
		data_prof_alias = profile_data["alias"]
		data_friend_events = []
		name_selected = data_prof_alias
		if(alias_requested != "" and alias_requested != data_prof_alias):
			name_selected = alias_requested
		print("name_selected", name_selected)
		firebase_id_selected = -1
		selected_user_data = {}
		if(validAlias(name_selected) == False):
			firebase_id_selected = aliasToFirebaseId(name_selected)
			selected_user_data = getProfileData(firebase_id_selected)
			selected_user_data["profile_picture"] = getProfilePictureFirebaseId(firebase_id_selected)
			print("firebase_id_selected", firebase_id_selected)
		else:
			return redir404(request)
		data_contact_list = getContactListData(user_firebase_id)
		database_contact_names = data_contact_list["contact_names"]
		if(database_contact_names == None):
			database_contact_names = []
		prof_mode = "friend"
		cal_mode = "USER"
		is_friend = "false"
		if name_selected == data_prof_alias:
			prof_mode = "self"
			cal_mode = "USER"
		else:
			prof_mode = "friend"
			cal_mode = "FRIEND"
			if firebase_id_selected in database_contact_names:
				is_friend = "true"
			else:
				is_friend = "false"

		database_calendar_dict = getCalendarDict(user_firebase_id, firebase_id_selected, cal_mode)
		if cal_mode == "FRIEND" and is_friend == "false":
			database_calendar_dict["calendar_data"]["member_events"] = []

		# HAO PUT AUTHORIZATION HERE
		# if can view calendar:
		calendarFrame = "sub_templates/calendarFrame.html"
		# else:
		# calendarFrame = "sub_templates/blankFrame.html"

		response = render(
			request=request,
			template_name=self.template_name,
			context={
				# PROFILE DATA
				"profile_forms" : getProfileForms(),
				"profile_mode" : prof_mode,
				"is_friend" : is_friend,
				"name_selected" : name_selected,
				"name_selected_data" : str(json.dumps(selected_user_data)),
				"user_database" : str(json.dumps(profile_data)),
				# HEADER DATA
				"header_forms" : getHeaderForms(),
				"user_header_database" : str(json.dumps(getHeaderDict(user_firebase_id))),
				# CALENDAR DATA
				"calendarFrame" : calendarFrame,
				"calendar_forms" : getCalendarForms(),
				"database_calendar_dict" : str(json.dumps(database_calendar_dict)),
			}
		)
		return response

	def get(self, request, alias):
		return self.dummy(request, alias)

	def post(self, request, alias):
		formController(request)
		switchType = request.POST.get('formType')
		if(switchType == "SubmitEvent"):
			return HttpResponseRedirect("/profile/");
		return self.dummy(request, alias)

# - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - -#

# EDIT PROFILE

def redirForce(request):
	e = EditProfileView()
	return e.get(request)

class EditProfileView(TemplateView):
	template_name = 'user_interface/edit_profile.html'

	def dummy(self, request):
		search_form = SearchForm()
		group_form = GroupForm()
		edit_form = EditProfileForm()
		user_firebase_id = getCurrentFirebaseId(request)
		isValid = validFirebaseId(user_firebase_id);
		print("isvalid_id", isValid)
		profile_json = ""
		if(isValid == False):
			profile_data = getProfileData(user_firebase_id)
			profile_data["profile_picture"] = getProfilePictureFirebaseId(user_firebase_id)
			profile_json = str(json.dumps(profile_data))
		else:
			profile_data = {}
			profile_data["profile_picture"] = getProfilePictureFirebaseId("-1")
			profile_json = str(json.dumps(profile_data))


		response = render(
			request=request,
			template_name=self.template_name,
			context={
			# EDIT PROFILE DATA
			"edit_form" : edit_form,
			"profile_info" : profile_json,
			# HEADER DATA
			"header_forms" : getHeaderForms(),
			"user_header_database" : str(json.dumps(getHeaderDict(user_firebase_id))),
			}
		)
		return response

	def get(self, request):
		return self.dummy(request)

	def post(self, request):
		formController(request)
		print("\n REDIR HOME \n")
		return redirect('/')

# - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - -#

# GROUP

def nullGroup(request):
	g = GroupView()
	if(request.method == "POST"):
		return g.post(request, "")
	return g.get(request, "")

class GroupView(TemplateView):
	template_name = 'user_interface/group.html'

	def dummy(self, request, group_name):
		user_firebase_id = getCurrentFirebaseId(request)
		isValid = validFirebaseId(user_firebase_id)
		print("isvalid_id", isValid)
		if(isValid == True):
			return redirForce(request)
		name_requested = group_name
		if(validGroupName(group_name) == True):
			return redir404(request)
		search_form = SearchForm()
		group_form = GroupForm()
		group_data = getGroupData(group_name)
		cal_mode = "GROUP"
		database_calendar_dict = getCalendarDict(user_firebase_id, group_name, cal_mode)
		return render(
			request=request,
			template_name=self.template_name,
			context={"search_form" : search_form, 
				"calendarFrame" : "sub_templates/calendarFrame.html",
				"group_form" : group_form,
				"calendar_mode" : "group",
				"name_requested" : name_requested,
				"group_data" : str(json.dumps(group_data)),
				"user_header_database" : str(json.dumps(getHeaderDict(user_firebase_id))),
				"calendar_forms" : getCalendarForms(),
				"database_calendar_dict" : str(json.dumps(database_calendar_dict)),
				"header_forms" : getHeaderForms(),
				}
		)


	def get(self, request, group_name):
		print("GROUP NAME:", group_name)
		return self.dummy(request, group_name)

	def post(self, request, group_name):
		print("GROUP NAME:", group_name)
		formController(request)
		switchType = request.POST.get('formType')
		if(switchType == "SubmitEvent"):
			return HttpResponseRedirect("/profile/");
		return self.dummy(request, group_name)

class DefaultView(TemplateView):
	template_name = 'user_interface/default.html'

	def get(self, request):
		return render(
			request=request,
			template_name=self.template_name,
			context={}
		)

# - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - -#

# SEARCH

def getBlankSearchDict():
	retDict = {
		"events" : [],
		"friends" : [],
		"users" : [],
		"groups" :[]
	}
	return retDict

def getSearchDict(search_term, user_firebase_id):
	retDict = getBlankSearchDict()
	isValid = validFirebaseId(user_firebase_id)
	if(isValid == True):
		return retDict
	temp_events = searchEvents(search_term)
	user_contact_list = getContactListData(user_firebase_id)
	temp_contacts = []
	if(user_contact_list["contact_names"] != None):
		temp_contacts = searchContacts(search_term, user_firebase_id)
	temp_users = searchUsers(search_term)
	temp_groups = searchGroups(search_term)
	print("temp_events", temp_events)
	print("temp_contacts", temp_contacts)
	print("temp_users", temp_users)
	print("temp_groups", temp_groups)
	return retDict

class SearchView(TemplateView):
	template_name = 'user_interface/search.html'

	def dummy(self, request, search_dict):
		user_firebase_id = getCurrentFirebaseId(request)
		isValid = validFirebaseId(user_firebase_id)
		if(isValid == True):
			return redirForce(request)
		return render(
			request=request,
			template_name=self.template_name,
			context={
				"search_data" : str(json.dumps(search_dict)),
				"user_header_database" : str(json.dumps(getHeaderDict(user_firebase_id))),
				"header_forms" : getHeaderForms(),
			}
		)

	def get(self, request):
		# NEEDS SUPPORT
		search_dict = getBlankSearchDict()
		return self.dummy(request, search_dict)

	def post(self, request):
		formController(request)
		formType = request.POST.get('formType')
		search_dict = getBlankSearchDict()
		if(formType == "SearchTerm"):
			search_form = SearchForm(request.POST)
			user_firebase_id = getCurrentFirebaseId(request)
			search_term = search_form["SIstring"].value()
			search_dict = getSearchDict(search_term, user_firebase_id)
		return self.dummy(request, search_dict)
		

# - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - -#

# FORM CONTROL

def formController(request):
	switchType = request.POST.get('formType')
	user_firebase_id = getCurrentFirebaseId(request)
	print(switchType)
	#SearchTerm
	if(switchType == "FriendResponse"):
		respondFriend(request)
	elif(switchType == "SubmitEvent"):
		submitEvent(request)
	elif(switchType == "FriendRequest"):
		friend_form = FriendRequestForm(request.POST)
		print(friend_form)
		add_alias = friend_form["FIreqalias"].value()
		print(add_alias)
		sendFriendRequestUI(user_firebase_id, add_alias)
	elif(switchType == "FriendRemove"):
		removeFriend(request)
	elif(switchType == "GroupRequest"):
		invite_form = GroupInviteForm(request.POST)
		print(invite_form)
	elif(switchType == "EditProfile"):
		editProfile(request)
	elif(switchType == "CreateGroup"):
		createGroupLocal(request)

def respondFriend(request):
	friend_response_form = FriendRespondRequest(request.POST)
	print(friend_response_form)
	invite_id = friend_response_form["FIinvite_id"].value()
	action_s = friend_response_form["FIaction"].value()
	action = False
	if(action_s == "accept"):
		action = True
	else:
		action = False
	actionFriendRequest(invite_id, action)

def submitEvent(request):
	user_firebase_id = getCurrentFirebaseId(request)
	event_form = EventForm(request.POST)
	event_name = event_form['EIname'].value()
	event_desc = event_form['EIdescription'].value()
	event_start = event_form['EIstart'].value()
	event_end = event_form['EIend'].value()
	invite = event_form['EIinvite'].value().split(",")
	invite_ids = []
	for alias in invite:
		valid_alias = validAlias(alias)
		if(valid_alias == False):
			# In database
			f_id = aliasToFirebaseId(alias)
			invite_ids.append(str(f_id))

	whitelist = event_form['EIwhitelist'].value().split(",")
	whitelist_ids = []
	for alias in whitelist:
		valid_alias = validAlias(alias)
		if(valid_alias == False):
			# In database
			f_id = aliasToFirebaseId(alias)
			whitelist_ids.append(str(f_id))

	blacklist = event_form['EIblacklist'].value().split(",")
	blacklist_ids = []
	for alias in blacklist:
		valid_alias = validAlias(alias)
		if(valid_alias == False):
			# In database
			f_id = aliasToFirebaseId(alias)
			blacklist_ids.append(str(f_id))

	repeat = event_form['EIrepeat'].value()
	repeat_pattern = event_form['EIrepeat_pattern'].value()
	if(repeat != "true" or repeat_pattern == "0000000"):
		createEvent(event_name, event_desc, [user_firebase_id], [user_firebase_id], whitelist_ids, blacklist_ids, 
			int(event_start), int(event_end), str(user_firebase_id))
	else:
		createRepeatEvent(event_name, event_desc, [user_firebase_id], [user_firebase_id], whitelist_ids, blacklist_ids,
			int(event_start), int(event_end), str(user_firebase_id), "weekly", int(event_start), int(event_end), repeat_pattern)

def sendFriendRequestUI(sender_firebase_id, reciever_alias):
	reciever_firebase_id = aliasToFirebaseId(reciever_alias)
	sendFriendRequest(sender_firebase_id, reciever_firebase_id)

def editProfile(request):
	firebase_id = getCurrentFirebaseId(request)
	isValid = validFirebaseId(firebase_id)
	profile_form = EditProfileForm(request.POST)
	alias = profile_form['PIalias'].value()
	phone_num = [profile_form['PIphone'].value()]
	last_name = profile_form['PIlast'].value()
	first_name = profile_form['PIfirst'].value()
	email = [profile_form['PIemail'].value()]
	birth_date = profile_form['PIbirthday'].value()
	organization = profile_form['PIorganization'].value()
	user_desc = profile_form['PIdescription'].value()
	new_prof = profile_form['PIpicture'].value()
	saveProfilePictueBase64(firebase_id, new_prof)
	if(isValid == False):
		# Modify current user
		editProfileData(firebase_id, alias, phone_num, last_name, first_name,
		email, birth_date, organization, user_desc)
	else:
		createProfileData(firebase_id, alias, phone_num, last_name, first_name,
		email, birth_date, organization, user_desc)

def removeFriend(request):
	rem_form = FriendRemoveForm(request.POST)
	print(rem_form)
	rem_alias = rem_form["FIremalias"].value()
	print(rem_alias)
	user_firebase_id = getCurrentFirebaseId(request)
	friend_firebase_id = aliasToFirebaseId(rem_alias)
	removeContact(user_firebase_id, friend_firebase_id)

def createGroupLocal(request):
	firebase_id = getCurrentFirebaseId(request)
	group_form = GroupForm(request.POST)
	print(group_form)
	group_name = group_form["GIname"].value()
	group_desc = group_form["GIdescription"].value()
	group_invite = group_form["GIinvite"].value().split(",")
	# def createGroup(firebase_id, group_name, group_admin, group_members, group_desc)
	createGroup(firebase_id, group_name, [], [], group_desc)

def getSearchResults(request):
	search_form = SearchForm(request.POST)
	user_firebase_id = getCurrentFirebaseId(request)
	print(search_form)



# - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - -#

# AUTHORIZATION DATA

def getCurrentFirebaseId(request):
	return request.user.username;