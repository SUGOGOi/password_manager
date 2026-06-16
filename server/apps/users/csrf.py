# apps/users/csrf.py
from django.http import HttpResponse
from django.views.decorators.csrf import csrf_exempt, ensure_csrf_cookie


def get_csrf_token(request):
    return HttpResponse()


get_csrf_token = csrf_exempt(get_csrf_token)
get_csrf_token = ensure_csrf_cookie(get_csrf_token)
