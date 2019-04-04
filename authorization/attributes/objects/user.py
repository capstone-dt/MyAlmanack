from .. import Object

# Django
from django.contrib.auth import get_user_model


class User(Object):
    _root = get_user_model()