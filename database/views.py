from django.shortcuts import render
from database.models import *
from django.db import connection
from django.db.models import Max
from django.contrib.postgres.search import TrigramSimilarity
from django.db.models.functions import Greatest
from fuzzywuzzy import process
from operator import itemgetter
import time

# Query database using an alias to get the firebase_id.
def aliasToFirebaseId(alias):
	firebase_id = Profile.objects.get(alias = alias).firebase_id
	return firebase_id

# Query database using a firebase_id to get the alias.
def firebaseIdToAlias(firebase_id):
	alias = Profile.objects.get(firebase_id = firebase_id).alias
	return alias

# INVITES
# Generate invite_id based off the max id-value in the invite_id column.
def generateInviteId():
	if Invite.objects.all().count() == 0:
		return 0
	else:
		max_id_val = Invite.objects.aggregate(Max('invite_id'))
		return max_id_val['invite_id__max'] + 1


# FRIEND REQUESTS
# Insert incoming / outgoing requests.
def sendFriendRequest(sender_firebase_id, receiver_firebase_id):
	with connection.cursor() as cursor:
		current_time = time.time()
		i_id = generateInviteId()
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
def actionFriendRequest(invite_id, accept):
	with connection.cursor() as cursor:
		# Get sender and receiver firebase_ids using invite_id via raw SQL query.
		cursor.execute('SELECT receiver_id, sender_id FROM "User_Request" WHERE invite_id = (SELECT CAST (%s AS SMALLINT))',
			[invite_id])
		ur = cursor.fetchone()
		# Get contact_list_ids for receiver and sender from Django models.
		receiver_firebase_id = ur[0]
		sender_firebase_id = ur[1]
		receiver_cl_id = Profile.objects.get(pk=receiver_firebase_id).contact_list_id
		sender_cl_id = Profile.objects.get(pk=sender_firebase_id).contact_list_id

		if accept == True:
			# If user request acceptance is true, then update the sender's and receiver's (of the user request) contact_names.
			# Else, do nothing.
			cursor.execute('UPDATE "Contact_List" SET contact_names = array_append(contact_names, %s)'
				+ ' WHERE contact_list_id = %s', [sender_firebase_id, receiver_cl_id])
			cursor.execute('UPDATE "Contact_List" SET contact_names = array_append(contact_names, %s)'
				+ ' WHERE contact_list_id = %s', [receiver_firebase_id, sender_cl_id])

		# Remove receiver's incoming user requests using raw SQL query.
		cursor.execute('UPDATE "Contact_List" SET received_friend_requests = array_remove(received_friend_requests, (SELECT CAST (%s AS SMALLINT)))'
			+ ' WHERE contact_list_id = %s', [invite_id, receiver_cl_id])
		# Remove sender's incoming user requests using raw SQL query.
		cursor.execute('UPDATE "Contact_List" SET sent_friend_requests = array_remove(sent_friend_requests, (SELECT CAST (%s AS SMALLINT)))'
			+ ' WHERE contact_list_id = %s', [invite_id, sender_cl_id])

# Get friend-request data based on invite_id.
def getFriendRequestData(invite_id):
	with connection.cursor() as cursor:
		cursor.execute('SELECT * FROM "User_Request" WHERE invite_id = %s', [invite_id])
		user_request_data = cursor.fetchone()
		# Return dictionary containing user-request information.
		user_request_cols = ['sender_id','receiver_id','time_sent','invite_id']
		user_request_data = dict((col, item) for col, item in zip(user_request_cols, user_request_data))
		return user_request_data


# EVENT INVITES
# Insert incoming / outgoing invites.
def sendEventInvites(sender_firebase_id, receiver_firebase_ids, event_id):
	with connection.cursor() as cursor:
		current_time = time.time()
		i_id = generateInviteId()
		# Get contact_list_ids for receiver and sender from Django models.
		receiver_cl_ids = [Profile.objects.get(firebase_id=fid).contact_list_id for fid in receiver_firebase_ids]
		sender_cl_id = Profile.objects.get(firebase_id=sender_firebase_id).contact_list_id
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
def actionEventInvite(invite_id, receiver_firebase_id, accept):
	with connection.cursor() as cursor:
		# Get event_id using invite_id via raw SQL query.
		cursor.execute('SELECT event_id FROM "Invite" NATURAL JOIN "Event_Invite"'
			+ ' WHERE invite_id = %s', [invite_id])
		event_id = cursor.fetchone()[0]
		# Get contact_list_id for receiver from Django models.
		receiver_cl_id = Profile.objects.get(firebase_id=receiver_firebase_id).contact_list_id

		if accept == True:
			# If event-invite acceptance is true, then update the receiver's user_events and the event's participating_users.
			# Else, do nothing.
			cursor.execute('UPDATE "Profile" SET user_events = array_append(user_events, %s)'
				+ ' WHERE firebase_id = %s', [event_id, receiver_firebase_id])
			cursor.execute('UPDATE "Event" SET participating_users = array_append(participating_users, %s)'
				+ ' WHERE event_id = %s', [receiver_firebase_id, event_id])

		# Remove receiver's incoming event-invites using raw SQL query.
		cursor.execute('UPDATE "Contact_List" SET received_event_invites = array_remove(received_event_invites, (SELECT CAST (%s AS SMALLINT)))'
			+ ' WHERE contact_list_id = %s', [invite_id, receiver_cl_id])

# Get event-invite data based on invite_id.
def getEventInviteData(invite_id):
	with connection.cursor() as cursor:
		cursor.execute('SELECT * FROM "Event_Invite" WHERE invite_id = %s', [invite_id])
		event_invite_data = cursor.fetchone()
		# Return dictionary containing event-invite information.
		event_invite_data_cols = ['time_sent','invite_id','event_id','invited_users']
		event_invite_data = dict((col, item) for col, item in zip(event_invite_data_cols, event_invite_data))
		return event_invite_data


# GROUP INVITES
# Insert incoming / outgoing invites.
def sendGroupInvites(group_id, receiver_firebase_ids):
	with connection.cursor() as cursor:
		current_time = time.time()
		i_id = generateInviteId()
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
def actionGroupInvite(invite_id, receiver_firebase_id, accept):
	with connection.cursor() as cursor:
		# Get group_name using invite_id via raw SQL query.
		cursor.execute('SELECT group_name FROM "Invite" NATURAL JOIN "Group_Invite"'
			+ ' WHERE invite_id = %s', [invite_id])
		group_id = cursor.fetchone()[0]
		# Get contact_list_id for receiver from Django models.
		receiver_cl_id = Profile.objects.get(firebase_id=receiver_firebase_id).contact_list_id

		if accept == True:
			# If group-invite acceptance is true, then update the receiver's memberships and the group's group_members.
			# Else, do nothing.
			cursor.execute('UPDATE "Contact_List" SET memberships = array_append(memberships, %s)'
				+ ' WHERE contact_list_id = %s', [group_id, receiver_cl_id])
			cursor.execute('UPDATE "Group" SET group_members = array_append(group_members, %s)'
				+ ' WHERE group_name = %s', [receiver_firebase_id, group_id])

		# Remove receiver's incoming group-invites using raw SQL query.
		cursor.execute('UPDATE "Contact_List" SET received_group_invites = array_remove(received_group_invites, (SELECT CAST (%s AS SMALLINT)))'
			+ ' WHERE contact_list_id = %s', [invite_id, receiver_cl_id])

# Get group-invite data based on invite_id.
def getGroupInviteData(invite_id):
	with connection.cursor() as cursor:
		cursor.execute('SELECT * FROM "Group_Invite" WHERE invite_id = %s', [invite_id])
		group_invite_data = cursor.fetchone()
		# Return dictionary containing group-invite information.
		group_invite_data_cols = ['group_name','invitee_list','time_sent','invite_id']
		group_invite_data = dict((col, item) for col, item in zip(group_invite_data_cols, group_invite_data))
		return group_invite_data


# GROUP REQUESTS
# Insert incoming / outgoing requests.
def sendGroupRequest(group_id, sender_firebase_id):
	with connection.cursor() as cursor:
		current_time = time.time()
		i_id = generateInviteId()
		# Get contact_list_id for sender from Django models.
		sender_cl_id = Profile.objects.get(firebase_id=sender_firebase_id).contact_list_id
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
def actionGroupRequest(invite_id, accept):
	with connection.cursor() as cursor:
		# Get group_name using invite_id via raw SQL query.
		cursor.execute('SELECT group_name, sender_id FROM "Invite" NATURAL JOIN "Group_Request"'
			+ ' WHERE invite_id = %s', [invite_id])
		gr = cursor.fetchone()
		group_id = gr[0]
		sender_firebase_id = gr[1]
		# Get contact_list_id for sender from Django models.
		sender_cl_id = Profile.objects.get(firebase_id=sender_firebase_id).contact_list_id

		if accept == True:
			# If group-request acceptance is true, then update the sender's memberships and the group's group_members.
			# Else, do nothing.
			cursor.execute('UPDATE "Contact_List" SET memberships = array_append(memberships, %s)'
				+ ' WHERE contact_list_id = %s', [group_id, sender_cl_id])
			cursor.execute('UPDATE "Group" SET group_members = array_append(group_members, %s)'
				+ ' WHERE group_name = %s', [sender_firebase_id, group_id])

		# Remove sender's incoming group-requests using raw SQL query.
		cursor.execute('UPDATE "Group" SET received_group_requests = array_remove(received_group_requests, (SELECT CAST (%s AS SMALLINT)))'
			+ ' WHERE group_name = %s', [invite_id, group_id])

# Get group-request data based on invite_id.
def getGroupRequestData(invite_id):
	with connection.cursor() as cursor:
		cursor.execute('SELECT * FROM "Group_Request" WHERE invite_id = %s', [invite_id])
		group_request_data = cursor.fetchone()
		# Return dictionary containing group-request information.
		group_request_data_cols = ['time_sent','invite_id','sender_id','group_name']
		group_request_data = dict((col, item) for col, item in zip(group_request_data_cols, group_request_data))
		return group_request_data


# USER DATA
# Get user data based on firebase_id.
def getProfileData(firebase_id):
	user_data = Profile.objects.filter(pk=firebase_id).values()[0]
	# Return dictionary containing profile information.
	return user_data

# Check for valid firebase_id.
def validFirebaseId(firebase_id):
	f_id = Profile.objects.filter(pk=firebase_id).count()
	valid_id = True

	if f_id > 0:
		valid_id = False

	return valid_id

# Check for valid alias.
def validAlias(alias):
	alias = Profile.objects.filter(alias=alias).count()
	valid_alias = True

	if alias > 0:
		valid_alias = False

	return valid_alias

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
		cl_id = generateContactListId()
		cursor.execute('INSERT INTO "Contact_List" (contact_list_id) VALUES (%s)', [cl_id])
		cursor.execute('INSERT INTO "Profile" (alias, phone_num, last_name, first_name, email, birth_date,'
			+ ' firebase_id, organization, contact_list_id, user_desc)'
			+ ' VALUES (%s,%s,%s,%s,%s,%s,%s,%s,%s,%s)',
			[alias, phone_num, last_name, first_name, email, birth_date, firebase_id, organization, cl_id, user_desc])

# Delete a user profile.
def deleteProfileData(firebase_id):
	with connection.cursor() as cursor:
		user_data = Profile.objects.filter(pk=firebase_id).values()[0]
		cl_id = user_data['contact_list_id']
		user_cl = ContactList.objects.filter(pk=cl_id)

		for f_id in user_cl.values()[0]['contact_names']:
			cursor.execute('UPDATE "Contact_List" SET contact_names = array_remove(contact_names, %s) '
				+ ' WHERE contact_list_id = %s', [firebase_id, Profile.objects.get(pk=f_id).contact_list_id])

		for g in user_cl.values()[0]['memberships']:
			cursor.execute('UPDATE "Group" SET group_members = array_remove(group_members, %s) '
				+ ' WHERE group_name = %s', [firebase_id, g])

		for sei in user_cl.values()[0]['sent_event_invites']:
			cursor.execute('')

# Return all aliases currently in the database.
def getAllAliases():
	return [item['alias'] for item in Profile.objects.all().values('alias')]

# CONTACT LIST
# Generate contact_list_id based off the max id-value in the contact_list_id column.
def generateContactListId():
	if ContactList.objects.all().count() == 0:
		return 0
	else:
		max_id_val = ContactList.objects.aggregate(Max('contact_list_id'))
		return max_id_val['contact_list_id__max'] + 1

# Get user's contact-list data based on firebase_id.
def getContactListData(firebase_id):
	cl_id = Profile.objects.filter(pk=firebase_id).values('contact_list_id')[0]['contact_list_id']
	contact_list_data = ContactList.objects.filter(pk=cl_id).values()[0]
	# Return dictionary containing contact-list information.
	return contact_list_data

# Remove contact from the user's contact-list using both the user and the contact's firebase_ids.
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

# Check for valid group_name.
def validGroupName(group_name):
	gn = Group.objects.filter(pk=group_name).count()
	valid_id = True

	if gn > 0:
		valid_id = False

	return valid_id

# Remove user from a group.
def leaveGroup(firebase_id, group_name):
	with connection.cursor() as cursor:
		# Get the contact_list_ids for both the user and the contact.
		user_cl_id = Profile.objects.filter(pk=firebase_id).values('contact_list_id')[0]['contact_list_id']
		# Remove user from the contact's contact_names and vice versa.
		cursor.execute('UPDATE "Contact_List" SET memberships = array_remove(memberships, %s)'
			+ 'WHERE contact_list_id=(SELECT CAST (%s AS SMALLINT))', [group_name, user_cl_id])
		cursor.execute('UPDATE "Group" SET group_members = array_remove(group_members, %s)'
			+ 'WHERE group_name=(SELECT CAST (%s AS SMALLINT))', [firebase_id, group_name])

# Return all group names currently in the database.
def getAllGroupNames():
	return [item['group_name'] for item in Group.objects.all().values('group_name')]

# Get group data based on group_name.
def getGroupData(group_name):
	group_data =  Group.objects.filter(pk=group_name).values()[0]
	# Return dictionary containing group data information.
	return group_data

# EVENTS
# Get all participating events of user and each event's corresponding details using firebase_id.
def getUserEvents(firebase_id):
	user_events_data = Profile.objects.filter(pk=firebase_id).values('user_events')[0]['user_events']
	# Get event details of each event.
	all_event_data = [Event.objects.filter(pk=e_id).values()[0] for e_id in user_events_data]
	# Return list of dictionaries containing event information.
	return all_event_data

# Generate event_id based off the max id-value in the event_id column.
def generateEventId():
	if Event.objects.all().count() == 0:
		return 0
	else:
		max_id_val = Event.objects.aggregate(Max('event_id'))
		return max_id_val['event_id__max'] + 1

# Get event data based on event_id.
def getEventData(event_id):
	event_data = Event.objects.filter(pk=event_id).values()[0]
	# Return dictionary containing event data information.
	return event_data

# Create an event and update the event creator's user_events.
def createEvent(event_title, description, participating_users, event_admins, whitelist, blacklist, start_date,
	end_date, event_creator_firebase_id):
	with connection.cursor() as cursor:
		event_id = generateEventId()
		# Create an event using a raw SQL query.
		cursor.execute('INSERT INTO "Event" (event_id, event_title, description, participating_users, event_admins,'
			+ ' whitelist, blacklist, start_date, end_date, event_creator_firebase_id) VALUES (%s,%s,%s,%s,%s,%s,%s,%s,%s,%s)',
			[event_id, event_title, description, participating_users, event_admins, whitelist, blacklist, start_date,
			end_date, event_creator_firebase_id])
		# Update event creator's users_events using a raw SQL query.
		cursor.execute('UPDATE "Profile" SET user_events = array_append(user_events, (SELECT CAST (%s AS SMALLINT))) WHERE firebase_id = %s',
			[event_id, event_creator_firebase_id])

# Create a repeat-event and update the repeat-event creator's user_events.
def createRepeatEvent(event_title, description, participating_users, event_admins, whitelist, blacklist,
	start_date, end_date, event_creator_firebase_id, rep_type, start_time, end_time, week_arr):
	with connection.cursor() as cursor:
		event_id = Event.objects.count()
		re_id = RepeatEvent.objects.count()
		# Create a repeat-event using a raw SQL query.
		cursor.execute('INSERT INTO "Repeat_Event" (event_id, event_title, description, participating_users, event_admins,'
			+ ' whitelist, blacklist, start_date, end_date, event_creator_firebase_id, rep_event_id,'
			+ ' rep_type, start_time, end_time, week_arr) VALUES (%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s)',
			[event_id, event_title, description, participating_users, event_admins, whitelist, blacklist, start_date,
			end_date, event_creator_firebase_id, re_id, rep_type, start_time, end_time, week_arr])
		# Update repeat-event creator's users_events using a raw SQL query.
		cursor.execute('UPDATE "Profile" SET user_events = array_append(user_events, (SELECT CAST (%s AS SMALLINT))) WHERE firebase_id = %s',
			[event_id, event_creator_firebase_id])

# Edit event data.
def editEventData(event_id, event_title, description, participating_users, event_admins, whitelist, blacklist, start_date,
	end_date):
	# Update event data via the Django Profile model.
	Event.objects.filter(pk=event_id).update(event_title=event_title,description=description,
		participating_users=participating_users, event_admins=event_admins, whitelist=whitelist,
		blacklist=blacklist, start_date=start_date, end_date=end_date)

# Edit repeat-event data.
def editRepeatEventData(event_id, rep_event_id, event_title, description, participating_users, event_admins, whitelist,
	blacklist, start_date, end_date, rep_type, week_arr, start_time, end_time):
	# Update repeat-event data via a raw SQL query.
	with connection.cursor() as cursor:
		cursor.execute('UPDATE "Repeat_Event" SET event_title = %s, description=%s, participating_users=%s, event_admins=%s,'
			+ ' whitelist=%s, blacklist=%s, start_date=%s, end_date=%s, rep_type=%s, start_time=%s, end_time=%s,'
			+ ' week_arr=%s WHERE event_id=%s',
			[event_title, description, participating_users, event_admins, whitelist, blacklist, start_date, end_date,
			rep_type, start_time, end_time, week_arr, event_id])

# Filter contact's events based on the values of whitelists or blacklists.
def getContactEvents(user_f_id, contact_f_id):
	# Get list of event_ids from a contact.
	contact_events_ids = Profile.objects.get(pk=contact_f_id).user_events
	# Get dictionary about each of the events' whitelists and blacklists
	# along with its corresponding event_id.
	contact_events_data = [Event.objects.filter(pk=c_e_id).values('event_id','whitelist',
		'blacklist')[0] for c_e_id in contact_events_ids]
	print(contact_events_data)

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

	# For every viewable contact event, get that event information and add it to a list.
	# Then, return the list of event data in a dictionary format.
	viewable_events_data = [Event.objects.filter(pk=ve).values()[0] for ve in viewable_events]
	return viewable_events_data


# SIMILARITY (search page) 
# Perform search queries on data based on Trigram Similarity.

# Search for events based on event_ids.
def searchEvents(search_term):
	# Run Trigram Similarity search on Event based on the search term.
	search = Event.objects.annotate(similarity=TrigramSimilarity('event_title', search_term)).filter(
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

# Search for groups based on group attributes.
def searchGroups(search_term):
	# Run Trigram Similarity search on Group based on the search term.
	search = Group.objects.annotate(similarity=TrigramSimilarity('group_name', search_term)).filter(
		similarity__gt=0.3).order_by('-similarity').values('group_name')
	# Return a list of group-names similar to the search term.
	return [item['group_name'] for item in search]
