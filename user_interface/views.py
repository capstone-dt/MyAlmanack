from django.views.generic import TemplateView
from django.shortcuts import render
from django.shortcuts import redirect
from django.http import HttpResponse
from django.contrib.auth.models import User
from database.views import *
from user_interface.forms import *
import base64
import os
import json
from authentication.firebase import get_session_claims
from django.contrib.auth import get_user_model
from django.contrib.auth.backends import ModelBackend


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

def getCurrUser(profile_json, firebase_id):
	# print("GET", firebase_id)
	for user in profile_json:
		# print(user["firebase_id"])
		if user["firebase_id"].replace(" ", "") == str(firebase_id).replace(" ", ""):
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

def getCurrentFirebaseId(request):
	return request.user.username;

def redirForce(request):
	e = EditProfileView()
	return e.get(request)

def redir404(request):
	user_firebase_id = getCurrentFirebaseId(request)
	return render(
		request=request,
		template_name='user_interface/404.html',
		context={"user_header_database" : str(json.dumps(getHeaderDict(user_firebase_id))),
			"header_forms" : getHeaderForms(),}
	)


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


def getFriendInfo(firebase_id):
	return None


def getFirebaseIDAliasDummy(user_structs, alias):
	for temp_user in user_structs:
		if(temp_user["alias"] == alias):
			return temp_user["firebase_id"]
	return -1


def getCalendarDict(user_firebase_id, selected_id, mode):
	retDict = {
		"mode" : "",
		"calendar_data" : {
			"user_events" : [],
			"member_events" : [],
			"member_info" : [],
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


def nullAlias(request):
	p = ProfileView()
	if(request.method == "POST"):
		return p.post(request, "")
	return p.get(request, "")

class ProfileView(TemplateView):
	template_name = 'user_interface/profile.html'

	def dummy(self, request, alias_requested):

		search_form = SearchForm()
		eventstructs = getDummyData("event_table")
		eventjson = str(json.dumps(eventstructs))
		profilestructs = getDummyData("profile_table")
		profilejson = str(json.dumps(profilestructs))
		contactstructs = getDummyData("contact_list_table")
		contactjson = str(json.dumps(contactstructs))

		user_firebase_id = getCurrentFirebaseId(request)
		isValid = validFirebaseId(user_firebase_id);
		print("isvalid_id", isValid)

		if(isValid == True):
			return redirForce(request)

		profile_data = getProfileData(user_firebase_id)
		profile_data["profile_picture"] = getProfilePictureFirebaseId(user_firebase_id)
		data_prof_alias = profile_data["alias"]
		print("data_prof_alias", data_prof_alias)
		# print(profile_data)
		profile_events = []
		try:
			if(profile_data['user_events'] != None):
				profile_events = getUserEvents(user_firebase_id)
		except:
			#don't add
			print("doesnt exist")
		print("profile_events", profile_events)
		data_contact_list = getContactListData(user_firebase_id)
		print("data_contact_list", data_contact_list)
		data_friend_events = []
		name_selected = data_prof_alias
		if(alias_requested != "" and alias_requested != data_prof_alias):
			#Other user selected
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
		print("validAlias:",name_selected, validAlias(name_selected), firebase_id_selected)

		database_calendar_dict = getCalendarDict(user_firebase_id, firebase_id_selected, cal_mode)
		if cal_mode == "FRIEND" and is_friend == "false":
			database_calendar_dict["calendar_data"]["member_events"] = []





		currentuserstruct = getCurrUser(profilestructs, user_firebase_id)
		# print(currentuserstruct)
		if bool(currentuserstruct[0]) == False:
			currentuserstruct = getCurrUser(profilestructs, "XJWoEcF4qsToA0NHnKnaIlqBnfO2")
		user_alias = currentuserstruct[0]["alias"]
		user_selected = currentuserstruct
		if(alias_requested != ""):
			# print("alias_requested:", alias_requested)
			user_alias = alias_requested
			name_selected = alias_requested
			sel_id = getFirebaseIDAliasDummy(profilestructs, alias_requested)
			user_selected = getCurrUser(profilestructs, sel_id)
			# print("user_selected", user_selected)


		currentuserjson = str(json.dumps(currentuserstruct))
		user_events = filterDummyEventsAlias(eventstructs, user_alias)
		user_contact_list_id = currentuserstruct[0]["contact_list_id"]
		user_contact_list = filterDummyContactsAlias(contactstructs, user_contact_list_id)
		friend_names = user_contact_list["contact_names"].replace(" ", "").split(",")
		# print(friend_names)
		friend_events = []

		for friend_alias in friend_names:
			curr_events = filterDummyEventsAlias(eventstructs, friend_alias)
			for temp_event in curr_events:
				friend_events.append(temp_event)
		filtered_friend_events = filterAccessFriendEvents(friend_events, currentuserstruct[0]["alias"])

		user_events_json = str(json.dumps(user_events))
		filtered_friend_events_json = str(json.dumps(filtered_friend_events))
		user_contact_list_json = str(json.dumps(user_contact_list))
		# print(user_contact_list)


		print("\n")
		def_prof_pic = getProfilePictureBase64("default_profile")
		response = render(
			request=request,
			template_name=self.template_name,
			context={
				"event_form" : EventForm(),
				"search_form" : search_form,
				"group_form" : GroupForm(),
				"dummy_events" : eventjson, 
				"dummy_profiles" : profilejson,
				"dummy_contacts" : contactjson,
				"user" : str(json.dumps(user_selected)),
				"user_events" : user_events_json,
				"member_events" : filtered_friend_events_json,
				"user_contact_list" : user_contact_list_json,
				"calendarFrame" : "sub_templates/calendarFrame.html",
				"default_profile" : def_prof_pic,
				"profile_mode" : prof_mode,
				"is_friend" : is_friend,
				"calendar_mode" : prof_mode,
				"name_selected" : name_selected,
				"name_selected_data" : str(json.dumps(selected_user_data)),
				"user_database" : str(json.dumps(profile_data)),
				"user_events_database" : str(json.dumps(profile_events)),
				"user_contact_list" : str(json.dumps(data_contact_list)),
				"user_header_database" : str(json.dumps(getHeaderDict(user_firebase_id))),
				"database_calendar_dict" : str(json.dumps(database_calendar_dict)),
				"header_forms" : getHeaderForms(),
				"friend_req" :  FriendRequestForm(),
				"friend_rem" : FriendRemoveForm(),
			}
		)
		return response

	def get(self, request, alias):
		print("alias passed:", alias)
		return self.dummy(request, alias)

	def post(self, request, alias):
		print("POST REQUESTED")
		formController(request)
		return self.dummy(request, alias)

class EditProfileView(TemplateView):
	template_name = 'user_interface/edit_profile.html'

	def dummy(self, request):
		search_form = SearchForm()
		group_form = GroupForm()
		edit_form = EditProfileForm()
		def_prof_pic = getProfilePictureBase64("default_profile")
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
			context={"edit_form" : edit_form, 
			"search_form" : search_form,
			"default_profile" : def_prof_pic,
			"profile_info" : profile_json,
			"user_header_database" : str(json.dumps(getHeaderDict(user_firebase_id))),
			"header_forms" : getHeaderForms(),
			"group_form" : group_form
			}
		)
		return response

	def get(self, request):
		return self.dummy(request)

	def post(self, request):
		formController(request)
		print("\n REDIR HOME \n")
		return redirect('/')


def nullGroup(request):
	g = GroupView()
	if(request.method == "POST"):
		return g.post(request, "")
	return g.get(request, "")


class GroupView(TemplateView):
	template_name = 'user_interface/group.html'

	def dummy(self, request, group_name):
		user_firebase_id = getCurrentFirebaseId(request)
		isValid = validFirebaseId(user_firebase_id);
		print("isvalid_id", isValid)
		if(isValid == True):
			return redirForce(request)
		name_requested = group_name
		if(validGroupName(group_name) == True):
			return redir404(request)
		search_form = SearchForm()
		group_form = GroupForm()
		group_data = getGroupData(group_name)
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
		return self.dummy(request, group_name)

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
		user_firebase_id = getCurrentFirebaseId(request)
		return render(
			request=request,
			template_name=self.template_name,
			context={"search_form" : search_form,
				"user_header_database" : str(json.dumps(getHeaderDict(user_firebase_id))),
			}
		)

	def post(self, request):
		search_form = SearchForm(request.POST)
		user_firebase_id = getCurrentFirebaseId(request)
		formController(request)
		return render(
			request=request,
			template_name=self.template_name,
			context={"search_form" : search_form,
				"events" : "[{}]",
				"friends" : "[{}]",
				"users" : "[{}]",
				"groups" : "[{}]",
				"user_header_database" : str(json.dumps(getHeaderDict(user_firebase_id))),
				"header_forms" : getHeaderForms(),
			}
		)

  
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
	elif(switchType == "SearchTerm"):
		return getSearchResults(request)

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
