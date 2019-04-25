# This is an auto-generated Django model module.
# You'll have to do the following manually to clean this up:
#   * Rearrange models' order
#   * Make sure each model has one field with primary_key=True
#   * Make sure each ForeignKey has `on_delete` set to the desired behavior.
#   * Remove `managed = False` lines if you wish to allow Django to create, modify, and delete the table
# Feel free to rename the models, but don't rename db_table values or field names.
from django.contrib.postgres.fields import ArrayField
from django.db import models


class ContactList(models.Model):
	contact_list_id = models.SmallIntegerField(primary_key=True)
	contact_names = ArrayField(models.CharField(max_length=128, blank=True, null=True))
	memberships = ArrayField(models.CharField(max_length=20, blank=True, null=True))
	sent_event_invites = ArrayField(models.SmallIntegerField(blank=True, null=True))
	received_event_invites = ArrayField(models.SmallIntegerField(blank=True, null=True))
	sent_friend_requests = ArrayField(models.SmallIntegerField(blank=True, null=True))
	received_friend_requests = ArrayField(models.SmallIntegerField(blank=True, null=True))
	sent_group_requests = ArrayField(models.SmallIntegerField(blank=True, null=True))
	received_group_invites = ArrayField(models.SmallIntegerField(blank=True, null=True))

	class Meta:
		managed = False
		db_table = 'Contact_List'


class Invite(models.Model):
	invite_id = models.SmallIntegerField(primary_key=True)
	time_sent = models.BigIntegerField()

	class Meta:
		abstract = True
		managed = False
		db_table = 'Invite'


class Event(models.Model):
	event_id = models.SmallIntegerField(primary_key=True)
	event_title = models.CharField(max_length=300)
	description = models.TextField(blank=True, null=True)
	participating_users = ArrayField(models.CharField(max_length=128, blank=True, null=True))
	event_admins = ArrayField(models.CharField(max_length=128))
	whitelist = ArrayField(models.CharField(max_length=128, blank=True, null=True))
	blacklist = ArrayField(models.CharField(max_length=128, blank=True, null=True))
	start_date = models.BigIntegerField()
	end_date = models.BigIntegerField()
	event_creator_firebase = models.ForeignKey('Profile', models.CASCADE)

	class Meta:
		managed = False
		db_table = 'Event'


class EventInvite(Invite):
	event_id = models.ForeignKey('Event', models.CASCADE, db_column='event_id')
	invited_users = ArrayField(models.CharField(max_length=128, blank=True, null=True))

	class Meta:
		managed = False
		db_table = 'Event_Invite'


class Group(models.Model):
	group_name = models.CharField(primary_key=True, max_length=20)
	group_admin = ArrayField(models.CharField(max_length=128))
	group_members = ArrayField(models.CharField(max_length=128))
	sent_group_invites = ArrayField(models.SmallIntegerField(blank=True, null=True))
	received_group_requests = ArrayField(models.SmallIntegerField(blank=True, null=True))
	group_desc = models.TextField(blank=True, null=True)

	class Meta:
		managed = False
		db_table = 'Group'


class GroupInvite(Invite):
	group_name = models.ForeignKey(Group, models.CASCADE, db_column='group_name')
	invitee_list = ArrayField(models.CharField(max_length=128, blank=True, null=True))

	class Meta:
		managed = False
		db_table = 'Group_Invite'

class GroupRequest(Invite):
    sender = models.ForeignKey('Profile', models.CASCADE)
    group_name = models.ForeignKey(Group, models.CASCADE, db_column='group_name')

    class Meta:
        managed = False
        db_table = 'Group_Request'

class Profile(models.Model):
	alias = models.CharField(unique=True, max_length=20)
	phone_num = ArrayField(models.CharField(max_length=11, blank=True, null=True))
	last_name = models.CharField(max_length=20)
	first_name = models.CharField(max_length=20)
	email = ArrayField(models.CharField(max_length=50, blank=True, null=True))
	contact_list = models.ForeignKey(ContactList, models.CASCADE)
	birth_date = models.BigIntegerField()
	firebase_id = models.CharField(max_length=128, primary_key=True)
	organization = models.CharField(max_length=255, blank=True, null=True)
	user_desc = models.TextField(blank=True, null=True)
	user_events = ArrayField(models.SmallIntegerField(blank=True, null=True))

	class Meta:
		managed = False
		db_table = 'Profile'
		unique_together = ('alias', 'firebase_id')


class RepeatEvent(Event):
	rep_event_id = models.SmallIntegerField(primary_key=True)
	rep_type = models.CharField(max_length=7)
	start_time = models.BigIntegerField()
	end_time = models.BigIntegerField()
	week_arr = models.CharField(max_length=7)

	class Meta:
		managed = False
		db_table = 'Repeat_Event'


class UserRequest(Invite):
	sender_id = models.CharField(max_length=128)
	receiver_id = models.CharField(max_length=128)

	class Meta:
		managed = False
		db_table = 'User_Request'


class AuthGroup(models.Model):
	name = models.CharField(unique=True, max_length=80)

	class Meta:
		managed = False
		db_table = 'auth_group'


class AuthGroupPermissions(models.Model):
	group = models.ForeignKey(AuthGroup, models.DO_NOTHING)
	permission = models.ForeignKey('AuthPermission', models.DO_NOTHING)

	class Meta:
		managed = False
		db_table = 'auth_group_permissions'
		unique_together = (('group', 'permission'),)


class AuthPermission(models.Model):
	name = models.CharField(max_length=255)
	content_type = models.ForeignKey('DjangoContentType', models.DO_NOTHING)
	codename = models.CharField(max_length=100)

	class Meta:
		managed = False
		db_table = 'auth_permission'
		unique_together = (('content_type', 'codename'),)


class AuthUser(models.Model):
	password = models.CharField(max_length=128)
	last_login = models.DateTimeField(blank=True, null=True)
	is_superuser = models.BooleanField()
	username = models.CharField(unique=True, max_length=150)
	first_name = models.CharField(max_length=30)
	last_name = models.CharField(max_length=150)
	email = models.CharField(max_length=254)
	is_staff = models.BooleanField()
	is_active = models.BooleanField()
	date_joined = models.DateTimeField()

	class Meta:
		managed = False
		db_table = 'auth_user'


class AuthUserGroups(models.Model):
	user = models.ForeignKey(AuthUser, models.DO_NOTHING)
	group = models.ForeignKey(AuthGroup, models.DO_NOTHING)

	class Meta:
		managed = False
		db_table = 'auth_user_groups'
		unique_together = (('user', 'group'),)


class AuthUserUserPermissions(models.Model):
	user = models.ForeignKey(AuthUser, models.DO_NOTHING)
	permission = models.ForeignKey(AuthPermission, models.DO_NOTHING)

	class Meta:
		managed = False
		db_table = 'auth_user_user_permissions'
		unique_together = (('user', 'permission'),)


class DjangoAdminLog(models.Model):
	action_time = models.DateTimeField()
	object_id = models.TextField(blank=True, null=True)
	object_repr = models.CharField(max_length=200)
	action_flag = models.SmallIntegerField()
	change_message = models.TextField()
	content_type = models.ForeignKey('DjangoContentType', models.DO_NOTHING, blank=True, null=True)
	user = models.ForeignKey(AuthUser, models.DO_NOTHING)

	class Meta:
		managed = False
		db_table = 'django_admin_log'


class DjangoContentType(models.Model):
	app_label = models.CharField(max_length=100)
	model = models.CharField(max_length=100)

	class Meta:
		managed = False
		db_table = 'django_content_type'
		unique_together = (('app_label', 'model'),)


class DjangoMigrations(models.Model):
	app = models.CharField(max_length=255)
	name = models.CharField(max_length=255)
	applied = models.DateTimeField()

	class Meta:
		managed = False
		db_table = 'django_migrations'


class DjangoSession(models.Model):
	session_key = models.CharField(primary_key=True, max_length=40)
	session_data = models.TextField()
	expire_date = models.DateTimeField()

	class Meta:
		managed = False
		db_table = 'django_session'
