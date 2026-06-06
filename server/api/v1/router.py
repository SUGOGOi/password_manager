from ninja import NinjaAPI
from apps.users.api import router as auth_router


api = NinjaAPI(title="Password Manager API", version="1.0.0", description="")


api.add_router("/auth", auth_router)
