from django.views.generic import TemplateView
from django.shortcuts import render
from django.http import HttpResponse
from django.contrib.auth.models import User
from user_interface.forms import EventForm
from user_interface.forms import EditProfileForm
from user_interface.forms import SearchForm
from database.models import *
from django.db import connection
from django.contrib.postgres.search import TrigramSimilarity
from django.db.models.functions import Greatest
from fuzzywuzzy import process
from operator import itemgetter
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
# Insert incoming / outgoing requests.
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

# Remove incoming / outgoing requests.
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
# Insert incoming / outgoing invites.
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

# Remove incoming / outgoing invites.
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
# Insert incoming / outgoing invites.
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
			
# Remove incoming / outgoing invites.
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
# Insert incoming / outgoing requests.
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

# Remove incoming / outgoing requests.
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
# Get user data based on firebase_id.
def getProfileData(firebase_id):
	user_data = Profile.objects.filter(pk=firebase_id).values()[0]
	# Return dictionary containing profile information.
	return user_data

# Edit user data.
def editProfileData(firebase_id, alias, phone_num, last_name, first_name,
	email, birth_date, organization, user_desc):
	# Update user data via the Django Profile model.
	Profile.objects.filter(pk=firebase_id).update(alias=alias, phone_num=phone_num,
		last_name=last_name,first_name=first_name, email=email, birth_date=birth_date,
		organization=organization, user_desc=user_desc)

# Create a profile and it's respective contact_list.
def createProfileData(firebase_id, alias, phone_num, last_name, first_name,
	email, birth_date, organization, user_desc):
	with connection.cursor() as cursor:
		cl_id = ContactList.objects.count()
		cursor.execute('INSERT INTO "Contact_List" (contact_list_id) VALUES (%s)', [cl_id])
		cursor.execute('INSERT INTO "Profile" (alias, phone_num, last_name, first_name, email, birth_date,'
			+ ' firebase_id, organization, contact_list_id, user_desc)'
			+ ' VALUES (%s,%s,%s,%s,%s,%s,%s,%s,%s,%s)',
			[alias, phone_num, last_name, first_name, email, birth_date, firebase_id, organization, cl_id, user_desc])

# CONTACT LIST
# Get user's contact-list data based on firebase_id.
def getContactListData(firebase_id):
	cl_id = Profile.objects.filter(pk=firebase_id).values('contact_list_id')[0]['contact_list_id']
	contact_list_data = ContactList.objects.filter(pk=cl_id).values()[0]
	# Return dictionary containing contact-list information.
	return contact_list_data

# Remove contact from the user's contact-list using both the user and the contact's
# firebase_ids.
def removeContact(user_id, contact_id):
	with connection.cursor() as cursor:
		# Get the contact_list_ids for both the user and the contact.
		user_cl_id = Profile.objects.filter(pk=user_id).values('contact_list_id')[0]['contact_list_id']
		contact_cl_id = Profile.objects.filter(pk=contact_id).values('contact_list_id')[0]['contact_list_id']
		# Remove user from the contact's contact_names and vice versa.
		cursor.execute('UPDATE "Contact_List" SET contact_names = array_remove(contact_names, %s)'
			+ 'WHERE contact_list_id=(SELECT CAST (%s AS SMALLINT))', [contact_id, user_cl_id])
		cursor.execute('UPDATE "Contact_List" SET contact_names = array_remove(contact_names, %s)'
			+ 'WHERE contact_list_id=(SELECT CAST (%s AS SMALLINT))', [user_id, contact_cl_id])

# GROUP
# Create an event and update the event creator's user_events.
def createGroup(firebase_id, group_name, group_admin, group_members, group_desc):
	with connection.cursor() as cursor:
		cl_id = Profile.objects.filter(pk=firebase_id).values('contact_list_id')[0]['contact_list_id']
		group_admin.insert(0, firebase_id)
		group_members.insert(0,firebase_id)
		cursor.execute('INSERT INTO "Group" (group_name, group_admin, group_members, group_desc) '
			+ ' VALUES (%s, %s, %s, %s)', [group_name, group_admin, group_members, group_desc])
		cursor.execute('UPDATE "Contact_List" SET memberships = array_append(memberships, %s)'
			+ ' WHERE contact_list_id = %s', [group_name, cl_id])

def leaveGroup(firebase_id, group_name):
	with connection.cursor() as cursor:
		# Get the contact_list_ids for both the user and the contact.
		user_cl_id = Profile.objects.filter(pk=firebase_id).values('contact_list_id')[0]['contact_list_id']
		# Remove user from the contact's contact_names and vice versa.
		cursor.execute('UPDATE "Contact_List" SET memberships = array_remove(memberships, %s)'
			+ 'WHERE contact_list_id=(SELECT CAST (%s AS SMALLINT))', [group_name, user_cl_id])
		cursor.execute('UPDATE "Group" SET group_members = array_remove(group_members, %s)'
			+ 'WHERE group_name=(SELECT CAST (%s AS SMALLINT))', [firebase_id, group_name])

# EVENTS
# Get all participating events of user and each event's corresponding details using firebase_id.
def getUserEvents(firebase_id):
	user_events_data = Profile.objects.filter(pk=firebase_id).values('user_events')[0]['user_events']
	# Get event details of each event.
	all_event_data = [Event.objects.filter(pk=e_id).values()[0] for e_id in user_events_data]
	# Return list of dictionaries containing event information.
	return all_event_data

# Create an event and update the event creator's user_events.
def createEvent(event_id, description, participating_users, event_admins, whitelist, blacklist, start_date,
	end_date, event_creator_firebase_id):
	with connection.cursor() as cursor:
		# Create an event using a raw SQL query.
		cursor.execute('INSERT INTO "Event" (event_id, description, participating_users, event_admins,'
			+ 'whitelist, blacklist, start_date, end_date, event_creator_firebase_id) VALUES (%s,%s,%s,%s,%s,%s,%s,%s,%s)',
			[event_id, description, participating_users, event_admins, whitelist, blacklist, start_date,
			end_date, event_creator_firebase_id])
		# Update event creator's users_events using a raw SQL query.
		cursor.execute('UPDATE "Profile" SET user_events = array_append(user_events, %s) WHERE firebase_id = %s',
			[event_id, event_creator_firebase_id])

# Create a repeat-event and update the repeat-event creator's user_events.
def createRepeatEvent(event_id, description, participating_users, event_admins, whitelist, blacklist,
	start_date, end_date, event_creator_firebase_id, rep_type, start_time, end_time, week_arr):
	with connection.cursor() as cursor:
		re_id = RepeatEvent.objects.count()
		# Create a repeat-event using a raw SQL query.
		cursor.execute('INSERT INTO "Repeat_Event" (event_id, description, participating_users, event_admins,'
			+ ' whitelist, blacklist, start_date, end_date, event_creator_firebase_id, rep_event_id,'
			+ ' rep_type, start_time, end_time, week_arr) VALUES (%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s)',
			[event_id, description, participating_users, event_admins, whitelist, blacklist, start_date,
			end_date, event_creator_firebase_id, re_id, rep_type, start_time, end_time, week_arr])
		# Update repeat-event creator's users_events using a raw SQL query.
		cursor.execute('UPDATE "Profile" SET user_events = array_append(user_events, %s) WHERE firebase_id = %s',
			[event_id, event_creator_firebase_id])

# Edit event data.
def editEventData(event_id, description, participating_users, event_admins, whitelist, blacklist, start_date,
	end_date):
	# Update event data via the Django Profile model.
	Event.objects.filter(pk=event_id).update(description=description,
		participating_users=participating_users, event_admins=event_admins, whitelist=whitelist,
		blacklist=blacklist, start_date=start_date, end_date=end_date)

# Edit repeat-event data.
def editRepeatEventData(event_id, rep_event_id, description, participating_users, event_admins, whitelist,
	blacklist, start_date, end_date, rep_type, week_arr, start_time, end_time):
	# Update repeat-event data via a raw SQL query.
	with connection.cursor() as cursor:
		cursor.execute('UPDATE "Repeat_Event" SET description=%s, participating_users=%s, event_admins=%s,'
			+ ' whitelist=%s, blacklist=%s, start_date=%s, end_date=%s, rep_type=%s, start_time=%s, end_time=%s,'
			+ 'week_arr=%s WHERE event_id=%s',
			[description, participating_users, event_admins, whitelist, blacklist, start_date, end_date,
			rep_type, start_time, end_time, week_arr, event_id])

# Filter contact's events based on the values of whitelists or blacklists.
def getContactEvents(user_f_id, contact_f_id):
	# Get list of event_ids from a contact.
	contact_events_ids = Profile.objects.get(pk=contact_f_id).user_events
	# Get dictionary about each of the events' whitelists and blacklists
	# along with its corresponding event_id.
	contact_events_data = [Event.objects.filter(pk=c_e_id).values('event_id','whitelist',
		'blacklist')[0] for c_e_id in contact_events_ids]

	contact_events_view_list = []
	viewable_events = []

	# Change any "None" values for whitelists or blacklists to an empty list.
	# Then, append each event_id and its respective whitelist and blacklist
	# to contact_events_view_list.
	for ced in contact_events_data:
		if ced['whitelist'] == None:
			ced['whitelist'] = []
		if ced['blacklist'] == None:
			ced['blacklist'] = []
		contact_events_view_list.append((ced['event_id'], ced['whitelist'], ced['blacklist']))

	# If a whitelist is not empty and a user is in the whitelist, then event is viewable.
	# Else if a blacklist is not empty and a user is not in the blacklist, then event
	# is viewable. Otherwise, the event is viewable to the user.
	for e_id, e_wl, e_bl in contact_events_view_list:
		if e_wl != []:
			if user_f_id in e_wl:
				viewable_events.append(e_id)
		elif e_bl != []:
			if user_f_id not in e_bl:
				viewable_events.append(e_id)
		else:
			viewable_events.append(e_id)

	return viewable_events


# SIMILARITY (search page) 
# Perform search queries on data based on Trigram Similarity.

# Search for events based on event_ids.
def searchEvents(search_term):
	# Run Trigram Similarity search on Event based on the search term.
	search = Event.objects.annotate(similarity=TrigramSimilarity('event_id', search_term)).filter(
		similarity__gt=0.3).order_by('-similarity').values('event_id')
	# Return a list of event_ids similar to the search term.
	return [item['event_id'] for item in search]

# Search for contacts based on user attributes.
def searchContacts(search_term, user_f_id):
	# Get all contact-names for a user via their firebase_id.
	user_contacts = ContactList.objects.get(pk=Profile.objects.get(pk=user_f_id).contact_list_id).contact_names
	# Get dictionaries of each contact's firebase_id, alias, first_name, and last_name.
	contact_info = [Profile.objects.filter(pk=c_f_id).values('firebase_id','alias','first_name',
		'last_name')[0] for c_f_id in user_contacts]
	sim_scores = []
	
	# Using firebase_id, alias, first_name, and last_name, extract the most accurate search results.
	for c in contact_info:
		c_arr = [c['firebase_id'], c['alias'], c['first_name'], c['last_name']]
		score = process.extractOne(search_term, c_arr)

		if score[1] > 0:
			sim_scores.append((score[1], c))

	# Sort results by highest accuracy.
	sim_scores = sorted(sim_scores, key=itemgetter(0), reverse=True)
	# Return a list of dictionaries containing an alias and a firebase_id along with the associated first_name
	# and last _name ther where the results where similar to the search term.
	return [item[1] for item in sim_scores]

# Search for users based on user attributes.
def searchUsers(search_term):
	# Run Trigram Similarity search on Profile's alias, firebase_id, first_name, and last name
	# to find a result with the greatest similarity, all based on the search term.
	search = Profile.objects.annotate(similarity=Greatest(
		TrigramSimilarity('alias', search_term),
		TrigramSimilarity('firebase_id', search_term),
		TrigramSimilarity('first_name', search_term),
		TrigramSimilarity('last_name', search_term))).filter(
	similarity__gt=0.3).order_by('-similarity').values('alias','firebase_id','first_name','last_name')
	# Return a list of dictionaries containing an alias and a firebase_id along with the associated first_name
	# and last _name ther where the results where similar to the search term.
	return [item for item in search]

def searchGroups(search_term):
	# Run Trigram Similarity search on Group based on the search term.
	search = Group.objects.annotate(similarity=TrigramSimilarity('group_name', search_term)).filter(
		similarity__gt=0.3).order_by('-similarity').values('group_name')
	# Return a list of group-names similar to the search term.
	return [item['group_name'] for item in search]
