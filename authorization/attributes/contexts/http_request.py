from .. import Context

# Django
from django.http.request import HttpRequest


class HttpRequestContext(Context):
    _root = HttpRequest