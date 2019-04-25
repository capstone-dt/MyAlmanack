from django.views.generic import TemplateView
from django.shortcuts import render
from django.shortcuts import redirect
from django.http import HttpResponse
from django.http import HttpResponseRedirect
from django.http import JsonResponse
from django.contrib.auth.models import User
from django.urls import resolve
from database.models import *
from database.views import *
from user_interface.forms import *
import base64
import os
import json
from authentication.firebase import get_session_claims
from django.contrib.auth import get_user_model
from django.contrib.auth.backends import ModelBackend
import authorization.api
from authentication.firebase import get_session_claims
from django.contrib.auth import get_user_model

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
	retDict["edit_event_form"] = EditEventForm()
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
	for ev in user_events:
		ev["event_creator_alias"] = firebaseIdToAlias(ev["event_creator_firebase_id"])
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
			filteredEvents = filterAccessFriendEvents(curr_events_friend, user_firebase_id)
			for ev in filteredEvents:
				ev["event_creator_alias"] = firebaseIdToAlias(ev["event_creator_firebase_id"])
				curr_dict_f["participating_events"].append(ev)
			member_events.append(curr_dict_f)
			member_info.append(member_profile_data)
		retDict["calendar_data"]["member_events"] = member_events
		retDict["calendar_data"]["member_info"] = member_info
	elif(mode == "FRIEND"):
		member_info = getProfileData(selected_id)
		friend_events = []
		if(member_info["user_events"] != None):
			friend_events = getUserEvents(selected_id)
		if(friend_events == None):
			friend_events = []
		curr_dict_f = {}
		curr_dict_f["firebase_id"] = selected_id
		curr_dict_f["participating_events"] = friend_events
		retDict["calendar_data"]["member_events"] = [curr_dict_f]
		retDict["calendar_data"]["member_info"] = [getProfileData(selected_id)]
	elif(mode == "GROUP"):
		print("group selected")
		group_name = selected_id
		retDict["calendar_data"]["member_events"] = []
		retDict["calendar_data"]["member_info"] = []
		if isMemberOfGroup(user_firebase_id, group_name) != True:
			return retDict
		group_data = getGroupData(group_name)
		for member in group_data["group_members"]:
			if member == user_firebase_id:
				continue
			member_info = getProfileData(member)
			retDict["calendar_data"]["member_info"].append(member_info)
			temp_events = []
			if(member_info["user_events"] != None):
				temp_events = getUserEvents(member)
			curr_dict_m = {}
			curr_dict_m["firebase_id"] = member
			curr_dict_m["participating_events"] = []
			is_friend = False
			data_contact_list = getContactListData(user_firebase_id)
			database_contact_ids = data_contact_list["contact_names"]
			if(database_contact_ids == None):
				database_contact_ids = []
			for friend_id in database_contact_ids:
				if(friend_id == member):
					is_friend = True
			if(is_friend == False):
				temp_events = genAllHiddenEvents(temp_events)
			else:
				temp_events = filterAccessFriendEvents(temp_events, user_firebase_id)
			for ev in temp_events:
				ev["event_creator_alias"] = firebaseIdToAlias(ev["event_creator_firebase_id"])
				curr_dict_m["participating_events"].append(ev)
			retDict["calendar_data"]["member_events"].append(curr_dict_m)
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

def genAllHiddenEvents(passed_events):
	retArray = []
	for ev in passed_events:
		retArray.append(genHiddenEvent(ev))
	return retArray

def filterAccessFriendEvents(friend_events, user_firebase_id):
	ret_filtered = []
	for temp_event in friend_events:
		whitelist = temp_event["whitelist"];
		blacklist = temp_event["blacklist"];
		whitelist_empty = False
		blacklist_empty = False
		if len(whitelist) == 0:
			whitelist_empty = True
		if len(blacklist) == 0:
			blacklist_empty = True
		if whitelist_empty and blacklist_empty == False:
			isblacklisted = False
			for blacklisted in blacklist:
				if blacklisted == user_firebase_id:
					isblacklisted = True
					break
			if isblacklisted:
				hiddenstruct = genHiddenEvent(temp_event)
				ret_filtered.append(hiddenstruct)
				continue
		if whitelist_empty == False and blacklist_empty:
			iswhitelisted = False
			for whitelisted in whitelist:
				if whitelisted == user_firebase_id:
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
		},
		"friend_info" :[],
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
		if(event_invite_ids == None):
			event_invite_ids = []
		for e_id in event_invite_ids:
			curr_event_invite_data = getEventInviteData(e_id)
			curr_event_data = getEventData(curr_event_invite_data["event_id"])
			event_owner_data = getProfileData(curr_event_data["event_creator_firebase_id"])
			curr_event_data["creator_data"] = event_owner_data
			curr_event_data["invite_id"] = e_id
			retHeader["event_invites"].append(curr_event_data)
	if(contact_list["received_friend_requests"] == None):
		retHeader["friend_requests"] = []
	else:
		friend_invite_ids = contact_list["received_friend_requests"]
		if(friend_invite_ids == None):
			friend_invite_ids = []
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
		if(group_invite_names == None):
			group_invite_names = []
		print("invite_ids", group_invite_names)
		for g_name in group_invite_names:
			request_data = getGroupInviteData(g_name)
			curr_group_data = getGroupData(request_data["group_name"])
			curr_group_data["invite_id"] = g_name
			retHeader["group_requests"]["invites"].append(curr_group_data)

	database_contact_ids = contact_list["contact_names"]
	if(database_contact_ids == None):
		database_contact_ids = []
	for f_id in database_contact_ids:
		curr_info = getProfileData(f_id)
		retHeader["friend_info"].append(curr_info)

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

def get_invite_data(request):
	user_firebase_id = getCurrentFirebaseId(request)
	data = getHeaderDict(user_firebase_id)
	return JsonResponse(data)

# - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - -#

# Error Pages

def redir404Arg(request, arg):
	return redir404(request)

def redir404(request):
	user_firebase_id = getCurrentFirebaseId(request)
	return render(
		request=request,
		template_name='user_interface/404.html',
		context={"user_header_database" : str(json.dumps(getHeaderDict(user_firebase_id))),
			"header_forms" : getHeaderForms(),}
	)

def redir403(request):
	user_firebase_id = getCurrentFirebaseId(request)
	return render(
		request=request,
		template_name='user_interface/403.html',
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

def redirFirebase(request, firebase_id_requested):
	isValidFb = validFirebaseId(firebase_id_requested)
	if isValidFb == True:
		return redir404(request)
	alias_requested = firebaseIdToAlias(firebase_id_requested)
	return HttpResponseRedirect("/profile/" + alias_requested)

def getFriendsInfo(user_firebase_id):
	retArray = []
	# Get contact list
	data_contact_list = getContactListData(user_firebase_id)
	# Get contact names
	database_contact_names = data_contact_list["contact_names"]
	if(database_contact_names == None):
		database_contact_names = []
	# Get contact data per contact name
	for f_id in database_contact_names:
		curr_struct = {}
		curr_prof_data = getProfileData(f_id)
		curr_struct["first_name"] = curr_prof_data["first_name"]
		curr_struct["last_name"] = curr_prof_data["last_name"]
		curr_struct["alias"] = curr_prof_data["alias"]
		curr_struct["firebase_id"] = curr_prof_data["firebase_id"]
		curr_struct["profile_picture"] = getProfilePictureFirebaseId(curr_prof_data["firebase_id"])
		retArray.append(curr_struct)
	return retArray

def getGroupsInfo(user_firebase_id):
	retArray = []
	# Get contact list
	data_contact_list = getContactListData(user_firebase_id)
	# Get memberships
	database_group_names = data_contact_list["memberships"]
	if(database_group_names == None):
		database_group_names = []
	# Get group data per membership
	for g_name in database_group_names:
		curr_struct = {}
		curr_group_data = getGroupData(g_name)
		curr_struct["group_name"] = curr_group_data["group_name"]
		retArray.append(curr_struct)
	return retArray

class ProfileView(TemplateView):
	template_name = 'user_interface/profile.html'

	def dummy(self, request, alias_requested):

		user_firebase_id = getCurrentFirebaseId(request)
		isValid = validFirebaseId(user_firebase_id)
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
			selected_user_data["friends_info"] = getFriendsInfo(firebase_id_selected)
			selected_user_data["groups_info"] = getGroupsInfo(firebase_id_selected)
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
		is_requested = "false"
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
			sent_friend_requests = data_contact_list["sent_friend_requests"]
			if sent_friend_requests == None:
				sent_friend_requests = []
			for fq in sent_friend_requests:
				curr_fq_data = getFriendRequestData(fq)
				if curr_fq_data["receiver_id"] == firebase_id_selected:
					is_requested = "true"
					break


		database_calendar_dict = getCalendarDict(user_firebase_id, firebase_id_selected, cal_mode)
		if cal_mode == "FRIEND" and is_friend == "false":
			database_calendar_dict["calendar_data"]["member_events"] = []

		# HAO PUT AUTHORIZATION HERE
		# if can view calendar:
		user = None
		try:
			user = get_user_model().objects.get(username=firebase_id_selected)
		except get_user_model().DoesNotExist:
			return redir404(request)

		auth_result = authorization.api.authorize(
			request,
			action=authorization.api.actions.user.calendar.ViewUserCalendar,
			resource=user,
			redirect_403=False
		)

		calendarFrame = "sub_templates/calendarFrame.html"
		if(auth_result == False):
			calendarFrame = "sub_templates/blankFrame.html"
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
				"is_requested" : is_requested,
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
		response = formController(request)
		if response != None:
			return response
		return self.dummy(request, alias)

def validate_alias(request):
	alias = request.GET.get("alias", None)
	is_taken = (validAlias(alias) == False)
	if(alias.lower() == "edit"):
		is_taken = True;
	
	data = {
		"is_taken" : is_taken
	}
	return JsonResponse(data)

# - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - -#

# EDIT PROFILE

def redirForce(request):
	return HttpResponseRedirect("/profile/edit/")

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
		response = formController(request)
		if response != None:
			return response
		return self.dummy(request)

# - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - -#

# GROUP

def nullGroup(request):
	return redir404(request)

def redirGroupname(request, group_name_requested):
	if(validGroupName(group_name_requested) == True):
		return redir404(request)
	return HttpResponseRedirect("/group/" + group_name_requested)

def getGroupDict(user_firebase_id, group_name):
	retDict = {}
	if validGroupName(group_name) == True:
		return retDict
	group_data = getGroupData(group_name)
	retDict["group_name"] = group_data["group_name"]
	retDict["group_desc"] = group_data["group_desc"]
	retDict["members"] = []
	for member in group_data["group_members"]:
		curr_data = getProfileData(member)
		curr_data["profile_picture"] = getProfilePictureFirebaseId(member)
		retDict["members"].append(curr_data)
	retDict["admins"] = []
	for admin in group_data["group_admin"]:
		curr_data = getProfileData(admin)
		curr_data["profile_picture"] = getProfilePictureFirebaseId(admin)
		retDict["admins"].append(curr_data)
	retDict["status"] = "USER"
	if isAdminOfGroup(user_firebase_id, group_name):
		retDict["status"] = "ADMIN"
	elif isMemberOfGroup(user_firebase_id, group_name):
		retDict["status"] = "MEMBER"
	else:
		retDict["status"] = "USER"
	return retDict

def getGroupForms():
	retDict = {}
	retDict["join_group"] = GroupJoinForm()
	retDict["leave_group"] = GroupLeaveForm()
	return retDict

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
		cal_mode = "GROUP"
		database_calendar_dict = getCalendarDict(user_firebase_id, group_name, cal_mode)

		group_status = "USER"
		group_dict = getGroupDict(user_firebase_id, group_name)

		group = Group.objects.get(group_name=group_name)

		auth_result = authorization.api.authorize(
			request,
			action=authorization.api.actions.group.calendar.ViewGroupCalendar,
			resource=group,
			redirect_403=False
		)

		calendarFrame = "sub_templates/calendarFrame.html"
		if(auth_result == False):
			calendarFrame = "sub_templates/blankFrame.html"


		return render(
			request=request,
			template_name=self.template_name,
			context={
				"calendarFrame" : calendarFrame,
				"calendar_mode" : "group",
				"name_requested" : name_requested,
				"group_dict" : str(json.dumps(group_dict)),
				"group_forms" : getGroupForms(),
				"user_header_database" : str(json.dumps(getHeaderDict(user_firebase_id))),
				"calendar_forms" : getCalendarForms(),
				"database_calendar_dict" : str(json.dumps(database_calendar_dict)),
				"header_forms" : getHeaderForms(),
				}
		)


	def get(self, request, group_name):
		return self.dummy(request, group_name)

	def post(self, request, group_name):
		response = formController(request)
		if response != None:
			return response
		return self.dummy(request, group_name)

def isAdminOfGroup(firebase_id, group_name):
	if(validGroupName(group_name) == True):
		return False
	group_data = getGroupData(group_name)
	for admin in group_data["group_admin"]:
		if admin == firebase_id:
			return True
	return False

def isMemberOfGroup(firebase_id, group_name):
	if(validGroupName(group_name) == True):
		return False
	group_data = getGroupData(group_name)
	for member in group_data["group_members"]:
		if member == firebase_id:
			return True
	return False

def validate_group_name(request):
	group_name = request.GET.get("group_name", None)
	is_taken = (validGroupName(group_name) == False)
	data = {
		"is_taken" : is_taken
	}
	return JsonResponse(data)

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

def getSearchForms():
	retDict = {}
	retDict["friend_req"] = FriendRequestForm();
	retDict["friend_rem"] = FriendRemoveForm();
	return retDict

def getBlankSearchDict():
	retDict = {
		"events" : [],
		"friends" : [],
		"users" : [],
		"groups" :[],
		"search_term" : "",
	}
	return retDict

def getSearchDict(search_term, user_firebase_id):
	retDict = getBlankSearchDict()
	isValid = validFirebaseId(user_firebase_id)
	if(isValid == True):
		return retDict
	temp_event_ids = searchEvents(search_term)
	temp_events = []
	for temp_id in temp_event_ids:
		temp_event_data = getEventData(temp_id)
		temp_event_data["event_creator_alias"] = firebaseIdToAlias(temp_event_data["event_creator_firebase_id"])
		temp_events.append(temp_event_data)
	user_contact_list = getContactListData(user_firebase_id)
	temp_contacts = []
	if(user_contact_list["contact_names"] != None):
		temp_contacts = searchContacts(search_term, user_firebase_id)
	for temp_contact in temp_contacts:
		temp_contact["isSelf"] = False
	temp_users_pre_filter = searchUsers(search_term)
	temp_users = []
	for temp_user in temp_users_pre_filter:
		if(temp_user["firebase_id"] == user_firebase_id):
			temp_user["isSelf"] = True
			temp_contacts = [temp_user] + temp_contacts
			break
	for temp_user in temp_users_pre_filter:
		contains = False
		for temp_contact in temp_contacts:
			if(temp_user["firebase_id"] == temp_contact["firebase_id"]):
				contains = True
				break
		if(contains == False and temp_user["firebase_id"] != user_firebase_id):
			temp_user["isSelf"] = False
			temp_users.append(temp_user)
	sent_friend_requests = user_contact_list["sent_friend_requests"]
	if sent_friend_requests == None:
		sent_friend_requests = []
	for temp_user in temp_users:
		temp_user["profile_picture"] = getProfilePictureFirebaseId(temp_user["firebase_id"])
		is_requested = False
		for fq in sent_friend_requests:
				curr_fq_data = getFriendRequestData(fq)
				if curr_fq_data["receiver_id"] == temp_user["firebase_id"]:
					is_requested = True
					break
		temp_user["isRequested"] = is_requested
	for temp_contact in temp_contacts:
		temp_contact["profile_picture"] = getProfilePictureFirebaseId(str(temp_contact["firebase_id"]))
	temp_group_names = searchGroups(search_term)
	temp_groups = []
	for group_name in temp_group_names:
		temp_groups.append(getGroupData(group_name))
	# print("temp_events", temp_events)
	# print("temp_contacts", temp_contacts)
	# print("temp_users", temp_users)
	# print("temp_groups", temp_groups)
	retDict["events"] = temp_events
	retDict["friends"] = temp_contacts
	retDict["users"] = temp_users
	retDict["groups"] = temp_groups
	retDict["search_term"] = search_term
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
				"search_forms" : getSearchForms(),
				"search_data" : str(json.dumps(search_dict)),
				"user_header_database" : str(json.dumps(getHeaderDict(user_firebase_id))),
				"header_forms" : getHeaderForms(),
			}
		)

	def get(self, request):
		# NEEDS SUPPORT
		search_dict = getBlankSearchDict()
		search_term = request.GET.get('q', '')
		# print("GET search_term:", search_term)
		if search_term != '':
			user_firebase_id = getCurrentFirebaseId(request)
			search_dict = getSearchDict(search_term, user_firebase_id)
		return self.dummy(request, search_dict)

	def post(self, request):
		response = formController(request)
		if response != None:
			return response
		return self.dummy(request, search_dict)
		

# - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - -#

# FORM CONTROL

def formController(request):
	switchType = request.POST.get('formType')
	user_firebase_id = getCurrentFirebaseId(request)
	print(switchType)
	#SearchTerm
	if(switchType == "FriendResponse"):
		res = respondFriend(request)
		if(res != None):
			return res
		return HttpResponseRedirect("/profile/")
	elif(switchType == "SubmitEvent"):
		res = submitEvent(request)
		if(res != None):
			return res
		return HttpResponseRedirect("/profile/")
	elif(switchType == "FriendRequest"):
		friend_form = FriendRequestForm(request.POST)
		print(friend_form)
		add_alias = friend_form["FIreqalias"].value()
		print(add_alias)
		res = sendFriendRequestUI(request, user_firebase_id, add_alias)
		if(res != None):
			return res
		return HttpResponseRedirect("/profile/" + add_alias)
	elif(switchType == "FriendRemove"):
		removeFriend(request)
		rem_form = FriendRemoveForm(request.POST)
		rem_alias = rem_form["FIremalias"].value()
		return HttpResponseRedirect("/profile/" + rem_alias)
	elif(switchType == "GroupRequest"):
		invite_form = GroupInviteForm(request.POST)
		print(invite_form)
	elif(switchType == "EditProfile"):
		editProfile(request)
		return HttpResponseRedirect("/profile/")
	elif(switchType == "CreateGroup"):
		res = createGroupLocal(request)
		if(res != None):
			return res
		group_form = GroupForm(request.POST)
		group_name = group_form["GIname"].value()
		return HttpResponseRedirect("/group/" + group_name)
	elif(switchType == "SearchTerm"):
		search_form = SearchForm(request.POST)
		search_term = search_form["SIstring"].value()
		return HttpResponseRedirect("/search/?q=" + search_term)
	elif(switchType == "JoinGroup"):
		group_form = GroupJoinForm(request.POST)
		group_name = group_form["GIreqname"].value()
		new_invite_id = generateInviteId(GroupInvite)
		sendGroupInvites(group_name, [user_firebase_id])
		actionGroupInvite(new_invite_id, user_firebase_id, True)
		return HttpResponseRedirect("/group/" + group_name)
	elif(switchType == "LeaveGroup"):
		group_form = GroupLeaveForm(request.POST)
		group_name = group_form["GIremname"].value()
		print(group_form)
		if isAdminOfGroup(user_firebase_id, group_name) == False:
			leaveGroup(user_firebase_id, group_name)
			return HttpResponseRedirect("/profile/")
		return HttpResponseRedirect("/group/" + group_name)
	elif(switchType == "EventResponse"):
		res = respondEvent(request)
		if(res != None):
			return res
		return HttpResponseRedirect("/profile/");
	elif(switchType == "GroupResponse"):
		res = respondGroup(request)
		if(res != None):
			return res
	elif(switchType == "SubmitEditEvent"):
		submitEditEvent(request)
		return HttpResponseRedirect("/profile/")

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

	req_data = getFriendRequestData(invite_id)
	sender_id = req_data["sender_id"]
	receiver_id = req_data["receiver_id"]

	user_request = None
	user_request = UserRequest.objects.get(invite_id=invite_id)

	if(action == True):
		# user.invite.AcceptUserInvite(subject=User|Profile, resource=UserRequest)
		auth_result = authorization.api.authorize(
			request,
			action=authorization.api.actions.user.request.AcceptUserRequest,
			resource=user_request,
			redirect_403=False
		)
		if(auth_result == False):
			return redir403(request)
	else:
		# user.invite.RejectUserInvite(subject=User|Profile, resource=UserRequest)
		auth_result = authorization.api.authorize(
			request,
			action=authorization.api.actions.user.request.RejectUserRequest,
			resource=user_request,
			redirect_403=False
		)
		if(auth_result == False):
			return redir403(request)

	actionFriendRequest(invite_id, action)

def submitEvent(request):
	user_firebase_id = getCurrentFirebaseId(request)
	event_form = EventForm(request.POST)
	print("EVENT SUBMIT:", event_form)
	event_name = event_form['EIname'].value()
	event_desc = event_form['EIdescription'].value()
	event_start = event_form['EIstart'].value()
	event_end = event_form['EIend'].value()
	invite_ids = []
	if(event_form['EIinvite'].value() != None and event_form['EIinvite'].value() != ""):
		invite_ids = event_form['EIinvite'].value().split(",")

	whitelist_ids = []
	if(event_form['EIwhitelist'].value() != None and event_form['EIwhitelist'].value() != ""):
		whitelist_ids = event_form['EIwhitelist'].value().split(",")
	
	blacklist_ids = []
	if(event_form['EIblacklist'].value() != None and event_form['EIblacklist'].value() != ""):
		blacklist_ids = event_form['EIblacklist'].value().split(",")
	
	event_id = generateEventId()
	print("EVENT_ID", event_id)

	repeat = event_form['EIrepeat'].value()
	repeat_pattern = event_form['EIrepeat_pattern'].value()
	if(repeat != "true" or repeat_pattern == "0000000"):
		createEvent(event_name, event_desc, [user_firebase_id], [user_firebase_id], whitelist_ids, blacklist_ids, 
			int(event_start), int(event_end), str(user_firebase_id))
	else:
		createRepeatEvent(event_name, event_desc, [user_firebase_id], [user_firebase_id], whitelist_ids, blacklist_ids,
			int(event_start), int(event_end), str(user_firebase_id), "weekly", int(event_start), int(event_end), repeat_pattern)

	if(len(invite_ids) > 0 and event_form['EIinvite'].value() != None):
		print("sendEventInvites(", user_firebase_id, invite_ids, event_id)
		sendEventInvites(user_firebase_id, invite_ids, event_id)

def submitEditEvent(request):
	edit_event_form = EditEventForm(request.POST)
	print("edit_event_form", edit_event_form)
	event_id = edit_event_form["EIediteventid"].value()
	event_name = edit_event_form["EIeditname"].value()
	event_desc = edit_event_form["EIeditdescription"].value()
	event_start = edit_event_form["EIeditstart"].value()
	event_end = edit_event_form["EIeditend"].value()
	# def editEventData(event_id, event_title, description, participating_users, event_admins, whitelist, blacklist, start_date,
	# end_date):
	# Get current event data
	curr_event_data = getEventData(event_id)
	participating_users = curr_event_data["participating_users"]
	event_admins = curr_event_data["event_admins"]
	whitelist = curr_event_data["whitelist"]
	blacklist = curr_event_data["blacklist"]

	# event.EditEvent(subject=User|Profile, resource=Event)
	event = None
	try:
		event = Event.objects.get(event_id=event_id)
	except:
		return redir404(request)

	auth_result = authorization.api.authorize(
		request,
		action=authorization.api.actions.event.EditEvent,
		resource=event,
		redirect_403=False
	)

	if(auth_result == False):
		return redir403(request)



	editEventData(event_id, event_name, event_desc, participating_users, event_admins, whitelist, blacklist, event_start, event_end)


def respondEvent(request):
	event_form = EventRespondRequest(request.POST)
	print(event_form)
	invite_id = event_form["EIinvite_id"].value()
	action_s = event_form["EIaction"].value()
	action = False
	if(action_s == "accept"):
		action = True
	else:
		action = False
	user_firebase_id = getCurrentFirebaseId(request)

	event_invite = None
	try:
		event_invite = EventInvite.objects.get(invite_id=invite_id)
	except:
		return redir404(request)

	if(action):
		# event.invite.AcceptEventInvite(subject=User|Profile, resource=EventInvite)
		auth_result = authorization.api.authorize(
			request,
			action=authorization.api.actions.event.invite.AcceptEventInvite,
			resource= event_invite,
			redirect_403=False
		)
		if(auth_result == False):
			return redir403(request)
	else:
		# event.invite.RejectEventInvite(subject=User|Profile, resource=EventInvite)
		auth_result = authorization.api.authorize(
			request,
			action=authorization.api.actions.event.invite.RejectEventInvite,
			resource= event_invite,
			redirect_403=False
		)
		if(auth_result == False):
			return redir403(request)

	actionEventInvite(int(invite_id), user_firebase_id, action)

def respondGroup(request):
	group_form = GroupRespondRequest(request.POST)
	print(group_form)
	invite_id = group_form["GIinvite_id"].value()
	action_s = group_form["GIaction"].value()
	action = False
	if(action_s == "accept"):
		action = True
	else:
		action = False
	user_firebase_id = getCurrentFirebaseId(request)
	# def actionGroupInvite(invite_id, receiver_firebase_id, accept):

	group_invite_data = getGroupInviteData(invite_id)

	group_name = group_invite_data["group_name"]

	group_invite = GroupInvite.objects.get(invite_id=invite_id)
	
	if(action):
		# group.invite.AcceptGroupInvite(subject=User|Profile, resource=GroupInvite)
		auth_result = authorization.api.authorize(
			request,
			action=authorization.api.actions.group.invite.AcceptGroupInvite,
			resource= group_invite,
			redirect_403=False
		)
		if(auth_result == False):
			return redir403(request)
	else:
		# group.invite.RejectGroupInvite(subject=User|Profile, resource=GroupInvite)
		auth_result = authorization.api.authorize(
			request,
			action=authorization.api.actions.group.invite.RejectGroupInvite,
			resource= group_invite,
			redirect_403=False
		)
		if(auth_result == False):
			return redir403(request)


	actionGroupInvite(invite_id, user_firebase_id, action)
	if(action):
		return HttpResponseRedirect("/group/" + group_name)
	return HttpResponseRedirect("/profile/")


def sendFriendRequestUI(request, sender_firebase_id, reciever_alias):
	reciever_firebase_id = aliasToFirebaseId(reciever_alias)

	user = None
	try:
		user = get_user_model().objects.get(username=reciever_firebase_id)
	except:
		return redir404(request)

	# user.invite.SendUserInvite(subject=User|Profile, resource=User|Profile)
	auth_result = authorization.api.authorize(
			request,
			action=authorization.api.actions.user.request.SendUserRequest,
			resource=user,
			redirect_403=False
		)
	if(auth_result == False):
		return redir403(request)

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
		# user.profile.EditUserProfile(subject=User|Profile, resource=User|Profile)
		user = None
		try:
			user = get_user_model().objects.get(username=firebase_id)
		except get_user_model().DoesNotExist:
			return redir404(request)

		auth_result = authorization.api.authorize(
			request,
			action=authorization.api.actions.user.profile.EditUserProfile,
			resource=user,
			redirect_403=False
		)

		editProfileData(firebase_id, alias, phone_num, last_name, first_name,
		email, birth_date, organization, user_desc)
	else:
		createProfileData(firebase_id, alias, phone_num, last_name, first_name,
		email, birth_date, organization, user_desc)

def removeFriend(request):
	rem_form = FriendRemoveForm(request.POST)
	rem_alias = rem_form["FIremalias"].value()
	user_firebase_id = getCurrentFirebaseId(request)
	friend_firebase_id = aliasToFirebaseId(rem_alias)
	removeContact(user_firebase_id, friend_firebase_id)

def createGroupLocal(request):
	firebase_id = getCurrentFirebaseId(request)
	group_form = GroupForm(request.POST)
	print(group_form)
	group_name = group_form["GIname"].value()
	group_desc = group_form["GIdescription"].value()
	group_invites = []
	if(group_form["GIinvite"].value() != "" and group_form["GIinvite"].value() != None ):
		group_invites = group_form["GIinvite"].value().split(",")
	# def createGroup(firebase_id, group_name, group_admin, group_members, group_desc)
	createGroup(firebase_id, group_name, [], [], group_desc)


	# group.invite.SendGroupInvite(subject=User|Profile, resource=Group)

	group = None
	try:
		group = Group.objects.get(group_name=group_name)
	except:
		return redir404(request)
	
	for inv in group_invites:
		user = None
		try:
			user = get_user_model().objects.get(username=inv)
		except get_user_model().DoesNotExist:
			return redir404(request)
		auth_result = authorization.api.authorize(
			request,
			action=authorization.api.actions.group.invite.SendGroupInvite,
			resource= user,
			context=group,
			redirect_403=False
		)
		if(auth_result == False):
			return redir403(request)
		sendGroupInvites(group_name, [inv])

# - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - -#

# AUTHORIZATION DATA

def getCurrentFirebaseId(request):
	return request.user.username;