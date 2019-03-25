from .. import Subject

# Django
from django.contrib.auth import get_user_model


class User(Subject):
    _root = get_user_model()