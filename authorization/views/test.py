import authorization.api

# MyAlmanack database (Justin's subsystem)
from database.models import Profile, Group

# Django
from django.http import HttpResponse
from django.utils.html import escape


def test(request):
    hao_uncg = Profile.objects.get(firebase_id="k8L2m8QQWMfc7zPwSzJr25AwdVB2")
    mike_capstonetest = Profile.objects.get(firebase_id="XJWoEcF4qsToA0NHnKnaIlqBnfO2")
    user = mike_capstonetest
    
    temp_group = Group.objects.get(group_name="tempgroup")
    group = temp_group
    
    authorization_requests = [
        # user.profile.ViewUserProfile
        authorization.api.AuthorizationRequest(request.user,
            action=authorization.api.actions.user.profile.ViewUserProfile,
            resource=user
        ),
        
        # user.profile.EditUserProfile
        authorization.api.AuthorizationRequest(request.user,
            action=authorization.api.actions.user.profile.EditUserProfile,
            resource=user
        ),
        
        # user.profile.DeleteUserProfile
        authorization.api.AuthorizationRequest(request.user,
            action=authorization.api.actions.user.profile.DeleteUserProfile,
            resource=user
        ),
        
        # user.calendar.ViewUserCalendar
        authorization.api.AuthorizationRequest(request.user,
            action=authorization.api.actions.user.calendar.ViewUserCalendar,
            resource=user
        ),
        
        # user.calendar.EditUserCalendar
        authorization.api.AuthorizationRequest(request.user,
            action=authorization.api.actions.user.calendar.EditUserCalendar,
            resource=user
        ),
        
        # user.request.SendUserRequest
        authorization.api.AuthorizationRequest(request.user,
            action=authorization.api.actions.user.request.SendUserRequest,
            resource=user
        ),
        
        # group.ViewGroup
        authorization.api.AuthorizationRequest(request.user,
            action=authorization.api.actions.group.ViewGroup,
            resource=group
        ),
        
        # group.EditGroup
        authorization.api.AuthorizationRequest(request.user,
            action=authorization.api.actions.group.EditGroup,
            resource=group
        ),
        
        # group.DeleteGroup
        authorization.api.AuthorizationRequest(request.user,
            action=authorization.api.actions.group.DeleteGroup,
            resource=group
        ),
        
        # group.calendar.ViewGroupCalendar
        authorization.api.AuthorizationRequest(request.user,
            action=authorization.api.actions.group.calendar.ViewGroupCalendar,
            resource=group
        ),
        
        # group.calendar.EditGroupCalendar
        authorization.api.AuthorizationRequest(request.user,
            action=authorization.api.actions.group.calendar.EditGroupCalendar,
            resource=group
        ),
        
        # group.invite.SendGroupInvite
        authorization.api.AuthorizationRequest(request.user,
            action=authorization.api.actions.group.invite.SendGroupInvite,
            resource=mike_capstonetest,
            context=group
        ),
        
        # group.request.SendGroupRequest
        authorization.api.AuthorizationRequest(request.user,
            action=authorization.api.actions.group.request.SendGroupRequest,
            resource=group
        ),
        
        # event.ViewEvent
    ]
    
    return HttpResponse("<br><br>".join(escape(
        "%s -> %s" %
        (authorization_request, authorization_request.authorize())
    ) for authorization_request in authorization_requests))