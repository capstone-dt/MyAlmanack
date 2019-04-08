from django.views.generic import TemplateView
from django.shortcuts import render
from django.http import HttpResponse
from django.contrib.auth.models import User
from user_interface.forms import EventForm
from user_interface.forms import EditProfileForm
from user_interface.forms import SearchForm
from database.models import *
from django.db import connection
import base64
import os
import json
import time

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
		print(request.session)
		users = User.objects.all()
		print(users)
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

		#sendGroupInvites('group2',['1','3','4'])
		#actionGroupInvite('group1','2',True)
		#actionGroupInvite('group1','3',False)
		sendGroupRequest('group1', '2')
		actionGroupRequest('group1', '2', True)
		print("Finished sending group invite")
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

# Query database using an alias to get the firebase_id.
def aliasToFirebaseId(alias):
	firebase_id = Profile.objects.get(alias = alias).firebase_id
	return firebase_id

# Query database using a firebase_id to get the alias.
def firebaseIdToAlias(firebase_id):
	alias = Profile.objects.get(firebase_id = firebase_id).alias
	return alias

# FRIEND REQUESTS
# insert incoming / outgoing
def sendFriendRequest(sender_firebase_id, receiver_firebase_id):
	with connection.cursor() as cursor:
		current_time = time.time()
		i_id = Invite.objects.count()
		# Get contact_list_ids for receiver and sender from Django models.
		receiver_cl_id = Profile.objects.get(firebase_id = receiver_firebase_id).contact_list_id
		sender_cl_id = Profile.objects.get(firebase_id = sender_firebase_id).contact_list_id
		# Create new user request using raw SQL query.
		cursor.execute('INSERT INTO "User_Request" (invite_id, time_sent, sender_id, receiver_id)'
			+ ' VALUES (%s, %s, %s, %s)',
			[i_id, current_time, sender_firebase_id, receiver_firebase_id])
		# Update receiver's incoming user requests using raw SQL query.
		cursor.execute('UPDATE "Contact_List" SET received_friend_requests = array_append(received_friend_requests, (SELECT CAST (%s AS SMALLINT)))'
			+ ' WHERE contact_list_id = %s', [i_id, receiver_cl_id])
		# Update sender's outgoing user requests using raw SQL query.
		cursor.execute('UPDATE "Contact_List" SET sent_friend_requests = array_append(sent_friend_requests, (SELECT CAST (%s AS SMALLINT)))'
			+ ' WHERE contact_list_id = %s', [i_id, sender_cl_id])

# remove incoming / outgoing
def actionFriendRequest(sender_firebase_id, receiver_firebase_id, accept):
	with connection.cursor() as cursor:
		# Get invite_id using sender and receiver firebase_ids using raw SQL query.
		cursor.execute('SELECT invite_id FROM "Invite" NATURAL JOIN "User_Request"'
			+ ' WHERE sender_id = %s and receiver_id = %s', [sender_firebase_id, receiver_firebase_id])
		i_id = cursor.fetchone()[0]
		# Get contact_list_ids for receiver and sender from Django models.
		receiver_cl_id = Profile.objects.get(firebase_id = receiver_firebase_id).contact_list_id
		sender_cl_id = Profile.objects.get(firebase_id = sender_firebase_id).contact_list_id

		if accept == True:
			# If user request acceptance is true, then update the sender's and receiver's (of the user request) contact_names.
			# Else, do nothing.
			cursor.execute('UPDATE "Contact_List" SET contact_names = array_append(contact_names, %s)'
				+ ' WHERE contact_list_id = %s', [sender_firebase_id, receiver_cl_id])
			cursor.execute('UPDATE "Contact_List" SET contact_names = array_append(contact_names, %s)'
				+ ' WHERE contact_list_id = %s', [receiver_firebase_id, sender_cl_id])

		# Remove receiver's incoming user requests using raw SQL query.
		cursor.execute('UPDATE "Contact_List" SET received_friend_requests = array_remove(received_friend_requests, (SELECT CAST (%s AS SMALLINT)))'
			+ ' WHERE contact_list_id = %s', [i_id, receiver_cl_id])
		# Remove sender's incoming user requests using raw SQL query.
		cursor.execute('UPDATE "Contact_List" SET sent_friend_requests = array_remove(sent_friend_requests, (SELECT CAST (%s AS SMALLINT)))'
			+ ' WHERE contact_list_id = %s', [i_id, sender_cl_id])

# EVENT INVITES
# insert incoming / outgoing
def sendEventInvites(sender_firebase_id, receiver_firebase_ids, event_id):
	with connection.cursor() as cursor:
		current_time = time.time()
		i_id = Invite.objects.count()
		# Get contact_list_ids for receiver and sender from Django models.
		receiver_cl_ids = [Profile.objects.get(firebase_id = fid).contact_list_id for fid in receiver_firebase_ids]
		sender_cl_id = Profile.objects.get(firebase_id = sender_firebase_id).contact_list_id
		# Create new event-invite using raw SQL query.
		cursor.execute('INSERT INTO "Event_Invite" (invite_id, time_sent, event_id)'
			+ ' VALUES (%s, %s, %s)',
			[i_id, current_time, event_id])

		# For every receiver firebase-id, update the invited_users list from the recently-created event-invite
		# using a raw SQL query.
		for f_id, r_cl_id in zip(receiver_firebase_ids, receiver_cl_ids):
			cursor.execute('UPDATE "Event_Invite" SET invited_users = array_append(invited_users, %s)'
				+ ' WHERE invite_id = %s', [f_id, i_id])
			cursor.execute('UPDATE "Contact_List" SET received_event_invites = array_append(received_event_invites, (SELECT CAST (%s AS SMALLINT)))'
				+ ' WHERE contact_list_id = %s', [i_id, r_cl_id])

		# Update sender's outgoing event-invites using raw SQL query.
		cursor.execute('UPDATE "Contact_List" SET sent_event_invites = array_append(sent_event_invites, (SELECT CAST (%s AS SMALLINT)))'
			+ ' WHERE contact_list_id = %s', [i_id, sender_cl_id])

# remove incoming / outgoing
def actionEventInvite(event_id, receiver_firebase_id, accept):
	with connection.cursor() as cursor:
		# Get invite_id using event_id using raw SQL query.
		cursor.execute('SELECT invite_id FROM "Invite" NATURAL JOIN "Event_Invite"'
			+ ' WHERE event_id = %s', [event_id])
		i_id = cursor.fetchone()[0]
		# Get contact_list_id for receiver from Django models.
		receiver_cl_id = Profile.objects.get(firebase_id = receiver_firebase_id).contact_list_id

		if accept == True:
			# If event-invite acceptance is true, then update the receiver's user_events and the event's participating_users.
			# Else, do nothing.
			cursor.execute('UPDATE "Profile" SET user_events = array_append(user_events, %s)'
				+ ' WHERE firebase_id = %s', [event_id, receiver_firebase_id])
			cursor.execute('UPDATE "Event" SET participating_users = array_append(participating_users, %s)'
				+ ' WHERE event_id = %s', [receiver_firebase_id, event_id])

		# Remove receiver's incoming event-invites using raw SQL query.
		cursor.execute('UPDATE "Contact_List" SET received_event_invites = array_remove(received_event_invites, (SELECT CAST (%s AS SMALLINT)))'
			+ ' WHERE contact_list_id = %s', [i_id, receiver_cl_id])

# GROUP INVITES
# insert incoming / outgoing
def sendGroupInvites(group_id, receiver_firebase_ids):
	with connection.cursor() as cursor:
		current_time = time.time()
		i_id = Invite.objects.count()
		# Get contact_list_id for receiver from Django models.
		receiver_cl_ids = [Profile.objects.get(firebase_id = fid).contact_list_id for fid in receiver_firebase_ids]
		# Create new event-invite using raw SQL query.
		cursor.execute('INSERT INTO "Group_Invite" (invite_id, time_sent, group_name)'
			+ ' VALUES (%s, %s, %s)',
			[i_id, current_time, group_id])

		# For every receiver firebase-id, update the invited_users list from the recently-created event-invite
		# using a raw SQL query.
		for f_id, r_cl_id in zip(receiver_firebase_ids, receiver_cl_ids):
			cursor.execute('UPDATE "Group_Invite" SET invitee_list = array_append(invitee_list, %s)'
				+ ' WHERE invite_id = %s', [f_id, i_id])
			cursor.execute('UPDATE "Contact_List" SET received_group_invites = array_append(received_group_invites, (SELECT CAST (%s AS SMALLINT)))'
				+ ' WHERE contact_list_id = %s', [i_id, r_cl_id])

		# Update sender's outgoing event-invites using raw SQL query.
		cursor.execute('UPDATE "Group" SET sent_group_invites = array_append(sent_group_invites, (SELECT CAST (%s AS SMALLINT)))'
			+ ' WHERE group_name = %s', [i_id, group_id])
			
# remove incoming / outgoing
def actionGroupInvite(group_id, receiver_firebase_id, accept):
	with connection.cursor() as cursor:
		# Get invite_id using group_id using raw SQL query.
		cursor.execute('SELECT invite_id FROM "Invite" NATURAL JOIN "Group_Invite"'
			+ ' WHERE group_name = %s', [group_id])
		i_id = cursor.fetchone()[0]
		# Get contact_list_id for receiver from Django models.
		receiver_cl_id = Profile.objects.get(firebase_id = receiver_firebase_id).contact_list_id

		if accept == True:
			# If group-invite acceptance is true, then update the receiver's memberships and the group's group_members.
			# Else, do nothing.
			cursor.execute('UPDATE "Contact_List" SET memberships = array_append(memberships, %s)'
				+ ' WHERE contact_list_id = %s', [group_id, receiver_cl_id])
			cursor.execute('UPDATE "Group" SET group_members = array_append(group_members, %s)'
				+ ' WHERE group_name = %s', [receiver_firebase_id, group_id])

		# Remove receiver's incoming group-invites using raw SQL query.
		cursor.execute('UPDATE "Contact_List" SET received_group_invites = array_remove(received_group_invites, (SELECT CAST (%s AS SMALLINT)))'
			+ ' WHERE contact_list_id = %s', [i_id, receiver_cl_id])

# GROUP REQUESTS
# insert incoming / outgoing
def sendGroupRequest(group_id, sender_firebase_id):
	with connection.cursor() as cursor:
		current_time = time.time()
		i_id = Invite.objects.count()
		# Get contact_list_id for sender from Django models.
		sender_cl_id = Profile.objects.get(firebase_id = sender_firebase_id).contact_list_id
		# Create new group-request using raw SQL query.
		cursor.execute('INSERT INTO "Group_Request" (invite_id, time_sent, sender_id, group_name)'
			+ ' VALUES (%s, %s, %s, %s)',
			[i_id, current_time, sender_firebase_id, group_id])
		# Update group's incoming group-requests using raw SQL query.
		cursor.execute('UPDATE "Group" SET received_group_requests = array_append(received_group_requests, (SELECT CAST (%s AS SMALLINT)))'
			+ ' WHERE group_name = %s', [i_id, group_id])
		# Update sender's outgoing group-requests using raw SQL query.
		cursor.execute('UPDATE "Contact_List" SET sent_group_requests = array_append(sent_group_requests, (SELECT CAST (%s AS SMALLINT)))'
			+ ' WHERE contact_list_id = %s', [i_id, sender_cl_id])

# remove incoming / outgoing
def actionGroupRequest(group_id, sender_firebase_id, accept):
	with connection.cursor() as cursor:
		# Get invite_id using group_id using raw SQL query.
		cursor.execute('SELECT invite_id FROM "Invite" NATURAL JOIN "Group_Request"'
			+ ' WHERE group_name = %s', [group_id])
		i_id = cursor.fetchone()[0]
		# Get contact_list_id for sender from Django models.
		sender_cl_id = Profile.objects.get(firebase_id = sender_firebase_id).contact_list_id

		if accept == True:
			# If group-request acceptance is true, then update the sender's memberships and the group's group_members.
			# Else, do nothing.
			cursor.execute('UPDATE "Contact_List" SET memberships = array_append(memberships, %s)'
				+ ' WHERE contact_list_id = %s', [group_id, sender_cl_id])
			cursor.execute('UPDATE "Group" SET group_members = array_append(group_members, %s)'
				+ ' WHERE group_name = %s', [sender_firebase_id, group_id])

		# Remove sender's incoming group-requests using raw SQL query.
		cursor.execute('UPDATE "Group" SET received_group_requests = array_remove(received_group_requests, (SELECT CAST (%s AS SMALLINT)))'
			+ ' WHERE group_name = %s', [i_id, group_id])

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

