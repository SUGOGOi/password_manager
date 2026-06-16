from ninja import Router
from django.http import HttpRequest
from django.shortcuts import get_object_or_404
from .models import Password
from .schemas import PasswordIn, PasswordOut, PasswordUpdateIn
from apps.users.auth import CookieAuth

router = Router(tags=["Todos"], auth=[CookieAuth()])


@router.get("/", response={200: list[PasswordOut], 401: dict})
def list_passwords(request: HttpRequest):
    todos = Password.objects.filter(user=request.auth)  # type: ignore
    return 200, list(todos)


@router.post("/", response={201: PasswordOut, 401: dict})
def create_password(request: HttpRequest, payload: PasswordIn):
    password = Password.objects.create(
        user=request.auth,  # type: ignore
        name=payload.name,
        username=payload.username,
        password=payload.password,
    )
    return 201, password


@router.get("/{password_id}", response={200: PasswordOut, 401: dict, 404: dict})
def get_password(request: HttpRequest, password_id: int):
    password = get_object_or_404(Password, id=password_id, user=request.auth)  # type: ignore
    return 200, password


@router.patch("/{password_id}", response={200: PasswordOut, 401: dict, 404: dict})
def update_password(request: HttpRequest, password_id: int, payload: PasswordUpdateIn):
    password = get_object_or_404(Password, id=password_id, user=request.auth)  # type: ignore

    # only update fields that were actually sent
    if payload.name is not None:
        password.name = payload.name
    if payload.username is not None:
        password.username = payload.username
    if payload.password is not None:
        password.password = payload.password

    password.save()
    return 200, password


@router.delete("/{password_id}", response={200: dict, 401: dict, 404: dict})
def delete_password(request: HttpRequest, password_id: int):
    password = get_object_or_404(Password, id=password_id, user=request.auth)  # type: ignore
    password.delete()
    return 200, {"message": "password deleted"}
