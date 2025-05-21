#api/v1/rbac.py

from uuid import UUID
from typing import List

from fastapi import APIRouter, Depends, status

from user_service.rbac.service import rbac_service
from user_service.rbac import schemas as rbac_schemas
from user_service.db import DBSessionDep
from user_service.api.deps import get_current_active_superuser

router = APIRouter(prefix="/rbac", tags=["RBAC"])


# ===== PERMISSIONS =====

@router.post(
    "/permissions",
    response_model=rbac_schemas.PermissionRead,
    status_code=status.HTTP_201_CREATED,
    dependencies=[Depends(get_current_active_superuser)]
)
async def create_permission(
    permission_in: rbac_schemas.PermissionCreate,
    conn: DBSessionDep,
):
    return await rbac_service.create_permission(conn, permission_in)


@router.get(
    "/permissions",
    response_model=List[rbac_schemas.PermissionRead],
    dependencies=[Depends(get_current_active_superuser)]
)
async def list_permissions(conn: DBSessionDep):
    return await rbac_service.get_all_permissions(conn)


# ===== ROLES =====

@router.post(
    "/roles",
    response_model=rbac_schemas.RoleRead,
    status_code=status.HTTP_201_CREATED,
    dependencies=[Depends(get_current_active_superuser)]
)
async def create_role(
    role_in: rbac_schemas.RoleCreate,
    conn: DBSessionDep,
):
    return await rbac_service.create_role(conn, role_in)


@router.get(
    "/roles",
    response_model=List[rbac_schemas.RoleRead],
    dependencies=[Depends(get_current_active_superuser)]
)
async def list_roles(conn: DBSessionDep):
    return await rbac_service.get_all_roles(conn)


@router.patch(
    "/roles/{role_id}",
    response_model=rbac_schemas.RoleRead,
    dependencies=[Depends(get_current_active_superuser)]
)
async def update_role(
    role_id: UUID,
    role_in: rbac_schemas.RoleUpdate,
    conn: DBSessionDep,
):
    return await rbac_service.update_role(conn, role_id, role_in)


# ===== USER ROLE ASSIGNMENT =====

@router.post(
    "/assign-roles",
    response_model=rbac_schemas.UserRoleRead,
    status_code=status.HTTP_200_OK,
    dependencies=[Depends(get_current_active_superuser)]
)
async def assign_roles(
    assignment: rbac_schemas.UserRoleAssignment,
    conn: DBSessionDep,
):
    return await rbac_service.assign_roles_to_user(
        conn, user_id=assignment.user_id, role_ids=assignment.role_ids
    )
