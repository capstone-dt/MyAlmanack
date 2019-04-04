from .. import Resource

# Django
from django.contrib.auth import get_user_model


class User(Resource):
    _root = get_user_model()