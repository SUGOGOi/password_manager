from ninja import Schema
from datetime import datetime


class PasswordIn(Schema):
    name: str
    username: str
    password: str


class PasswordOut(Schema):
    id: int
    name: str
    username: str
    password: str
    created_at: datetime
    updated_at: datetime


class PasswordUpdateIn(Schema):
    name: str | None = None
    username: str | None = None
    password: str | None = None
