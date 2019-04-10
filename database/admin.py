from django.contrib import admin
from .models import *
# Register your models here.

admin.site.register(ContactList)
admin.site.register(Invite)
admin.site.register(Event)
admin.site.register(EventInvite)
admin.site.register(Group)
admin.site.register(GroupInvite)
