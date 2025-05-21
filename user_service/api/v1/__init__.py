from fastapi import APIRouter
from . import user
from . import auth 
from . import rbac

api_v1_router = APIRouter(prefix="/v1")


# Include individual routers here
api_v1_router.include_router(user.router)
api_v1_router.include_router(auth.router)
api_v1_router.include_router(rbac.router)
