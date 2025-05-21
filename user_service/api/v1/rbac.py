#api/v1/rbac.py

from fastapi import APIRouter, Depends, status
from typing import List
from user_service.rbac import schemas as rbac_schemas
from user_service.rbac.service import RBACService
from user_service.api.deps import get_current_active_superuser
from user_service.auth.schemas import TokenPayload
from uuid import UUID

router = APIRouter(prefix="/rbac", tags=["RBAC"])

# -----------------------------
# Permission Endpoints
# -----------------------------

@router.post("/permissions", response_model=rbac_schemas.PermissionRead, status_code=status.HTTP_201_CREATED)
async def create_permission(
    permission: rbac_schemas.PermissionCreate,
    rbac_service: RBACService = Depends(),
    _: TokenPayload = Depends(get_current_active_superuser),
):
    return await rbac_service.create_permission(permission)


@router.get("/permissions", response_model=List[rbac_schemas.PermissionRead])
async def list_permissions(
    rbac_service: RBACService = Depends(),
    _: TokenPayload = Depends(get_current_active_superuser),
):
    return await rbac_service.get_all_permissions()


# -----------------------------
# Role Endpoints
# -----------------------------

@router.post("/roles", response_model=rbac_schemas.RoleRead, status_code=status.HTTP_201_CREATED)
async def create_role(
    role: rbac_schemas.RoleCreate,
    rbac_service: RBACService = Depends(),
    _: TokenPayload = Depends(get_current_active_superuser),
):
    return await rbac_service.create_role(role)


@router.get("/roles", response_model=List[rbac_schemas.RoleRead])
async def list_roles(
    rbac_service: RBACService = Depends(),
    _: TokenPayload = Depends(get_current_active_superuser),
):
    return await rbac_service.get_all_roles()


@router.put("/roles/{role_id}", response_model=rbac_schemas.RoleRead)
async def update_role(
    role_id: str,
    role_data: rbac_schemas.RoleUpdate,
    rbac_service: RBACService = Depends(),
    _: TokenPayload = Depends(get_current_active_superuser),
):
    return await rbac_service.update_role(role_id, role_data)


# -----------------------------
# Assign Role to User
# -----------------------------

@router.post("/users/{user_id}/roles", status_code=status.HTTP_200_OK)
async def assign_roles_to_user(
    user_id: UUID,
    data: rbac_schemas.UserRoleAssignment,
    rbac_service: RBACService = Depends(),
    _: TokenPayload = Depends(get_current_active_superuser),
):
    return await rbac_service.assign_roles_to_user(user_id, data.role_ids)
