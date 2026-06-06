from typing import Any

from django.http import HttpRequest
from ninja.security import APIKeyCookie
from django.contrib.auth import get_user_model
from jose import jwt, JWTError
import os


User = get_user_model()

SECRET_KEY = os.getenv("SECRET_KEY", "fallback-secret-key")


class CookieAuth(APIKeyCookie):
    param_name = "access_token"

    def authenticate(self, request: HttpRequest, key: str | None) -> Any | None:
        if not key:
            return None
        try:
            payload = jwt.decode(key, SECRET_KEY, algorithms=["HS256"])
            user_id = payload.get("user_id")
            if user_id is None:
                return None
            return User.objects.get(id=user_id)
        except (JWTError, User.DoesNotExist) as e:
            print("error:", e)
            return None
