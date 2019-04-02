C:\Users\oakle\MyAlmanack
['C:\\Users\\oakle\\MyAlmanack\\user_interface\\static']
# This is an auto-generated Django model module.
# You'll have to do the following manually to clean this up:
#   * Rearrange models' order
#   * Make sure each model has one field with primary_key=True
#   * Make sure each ForeignKey has `on_delete` set to the desired behavior.
#   * Remove `managed = False` lines if you wish to allow Django to create, modify, and delete the table
# Feel free to rename the models, but don't rename db_table values or field names.
from django.db import models


class ContactList(models.Model):
    contact_list_id = models.SmallIntegerField(primary_key=True)
    contact_names = models.TextField(blank=True, null=True)  # This field type is a guess.
    memberships = models.TextField(blank=True, null=True)  # This field type is a guess.
    sent_friend_requests = models.TextField(blank=True, null=True)  # This field type is a guess.
    received_friend_requests = models.TextField(blank=True, null=True)  # This field type is a guess.
    sent_group_requests = models.TextField(blank=True, null=True)  # This field type is a guess.
    received_group_requests = models.TextField(blank=True, null=True)  # This field type is a guess.
    sent_event_invites = models.TextField(blank=True, null=True)  # This field type is a guess.
    received_event_invites = models.TextField(blank=True, null=True)  # This field type is a guess.

    class Meta:
        managed = False
        db_table = 'Contact_List'


class Event(models.Model):
    event_id = models.CharField(primary_key=True, max_length=300)
    description = models.TextField(blank=True, null=True)
    participating_users = models.TextField(blank=True, null=True)  # This field type is a guess.
    event_admins = models.TextField()  # This field type is a guess.
    whitelist = models.TextField(blank=True, null=True)  # This field type is a guess.
    blacklist = models.TextField(blank=True, null=True)  # This field type is a guess.
    start_date = models.DateTimeField()
    end_date = models.DateTimeField()
    event_creator_alias = models.ForeignKey('Profile', models.DO_NOTHING, db_column='event_creator_alias')
    event_creator_firebase_id = models.CharField(max_length=128)

    class Meta:
        managed = False
        db_table = 'Event'


class EventInvite(models.Model):
    invite_id = models.SmallIntegerField()
    time_sent = models.DateTimeField()
    event = models.ForeignKey(Event, models.DO_NOTHING)
    invited_users = models.TextField(blank=True, null=True)  # This field type is a guess.
    event_creator_alias = models.ForeignKey('Profile', models.DO_NOTHING, db_column='event_creator_alias')
    event_creator_firebase_id = models.CharField(max_length=128)

    class Meta:
        managed = False
        db_table = 'Event_Invite'
        unique_together = (('invite_id', 'event', 'event_creator_alias', 'event_creator_firebase_id'),)


class Group(models.Model):
    group_name = models.CharField(primary_key=True, max_length=20)
    group_admin = models.TextField()  # This field type is a guess.
    group_members = models.TextField()  # This field type is a guess.
    incoming_requests = models.TextField(blank=True, null=True)  # This field type is a guess.
    outgoing_requests = models.TextField(blank=True, null=True)  # This field type is a guess.
    group_desc = models.TextField(blank=True, null=True)

    class Meta:
        managed = False
        db_table = 'Group'


class GroupInvite(models.Model):
    invite_id = models.SmallIntegerField()
    time_sent = models.DateTimeField()
    group_name = models.ForeignKey(Group, models.DO_NOTHING, db_column='group_name')
    invitee_list = models.TextField(blank=True, null=True)  # This field type is a guess.

    class Meta:
        managed = False
        db_table = 'Group_Invite'


class Invite(models.Model):
    invite_id = models.SmallIntegerField(primary_key=True)
    time_sent = models.DateTimeField()

    class Meta:
        managed = False
        db_table = 'Invite'


class Profile(models.Model):
    alias = models.CharField(primary_key=True, max_length=20)
    phone_num = models.TextField()  # This field type is a guess.
    last_name = models.CharField(max_length=20)
    first_name = models.CharField(max_length=20)
    email = models.TextField(blank=True, null=True)  # This field type is a guess.
    contact_list = models.ForeignKey(ContactList, models.DO_NOTHING)
    birth_date = models.DateField()
    firebase_id = models.CharField(unique=True, max_length=128)
    organization = models.CharField(max_length=255, blank=True, null=True)
    user_desc = models.TextField(blank=True, null=True)
    user_events = models.TextField(blank=True, null=True)  # This field type is a guess.

    class Meta:
        managed = False
        db_table = 'Profile'
        unique_together = (('alias', 'contact_list'), ('alias', 'firebase_id'),)


class RepeatEvent(models.Model):
    event_id = models.CharField(max_length=300)
    description = models.TextField(blank=True, null=True)
    participating_users = models.TextField(blank=True, null=True)  # This field type is a guess.
    event_admins = models.TextField()  # This field type is a guess.
    whitelist = models.TextField(blank=True, null=True)  # This field type is a guess.
    blacklist = models.TextField(blank=True, null=True)  # This field type is a guess.
    start_date = models.DateTimeField()
    end_date = models.DateTimeField()
    event_creator_alias = models.CharField(max_length=20)
    rep_event_id = models.SmallIntegerField(primary_key=True)
    rep_type = models.CharField(max_length=7)
    week_arr = models.TextField()  # This field type is a guess.
    start_time = models.TimeField()
    end_time = models.TimeField()
    event_creator_firebase_id = models.CharField(max_length=128)

    class Meta:
        managed = False
        db_table = 'Repeat_Event'
        unique_together = (('event_id', 'rep_event_id'),)


class UserRequest(models.Model):
    invite_id = models.SmallIntegerField()
    time_sent = models.DateTimeField()
    sender_alias = models.CharField(max_length=20)
    receiver_alias = models.CharField(max_length=20)

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
