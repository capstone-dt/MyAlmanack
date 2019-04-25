from django.contrib import admin
from django.urls import path, include

urlpatterns = [
    path('admin/', admin.site.urls),
    path("", include("authentication.urls")),
    # path("authorization/", include("authorization.urls")),
    path('', include('user_interface.urls')),
]