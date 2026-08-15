from fastapi import APIRouter, Depends, status
from sqlalchemy.ext.asyncio import AsyncSession

from adapters.repositories.adapter_user import AdapterUser
from application.use_cases.user import (create_user_case, get_user_case,
                                        get_users_case, remove_user_case,
                                        update_user_case)
from db.Session import get_db
from domain.user_models import CreateUser, GetUser
from schemas.user import UserField, UserResponse
from utils.response_util import to_response

router = APIRouter(
    prefix="/users",
    tags=["user"]
    )

@router.get("/", response_model=list[UserResponse])
async def get_users(db: AsyncSession = Depends(get_db)) -> list[UserResponse]:
    adapter = AdapterUser(db)
    result = await get_users_case(adapter)
    return [
      to_response(UserResponse, user)
      for user in result
    ]

@router.get("/{id}", response_model=UserResponse)
async def get_user(id: int, db: AsyncSession = Depends(get_db)) -> UserResponse:
    adapter = AdapterUser(db)
    request = GetUser(id=id)
    result = await get_user_case(request, adapter)
  
    return to_response(UserResponse, result)

@router.post(
  "/",
  response_model=UserResponse,
  status_code=status.HTTP_201_CREATED
)
async def create_user(user: UserField, db: AsyncSession = Depends(get_db)) -> UserResponse:
    adapter = AdapterUser(db)
    request = CreateUser(organization_id=user.organization_id,
                         email=user.email,
                         password_hash=user.password_hash,
                         first_name=user.first_name,
                         last_name=user.last_name,
                         role=user.role)
    result = await create_user_case(request, adapter)
    return to_response(UserResponse, result)

@router.put("/{id}", response_model=UserResponse)
async def update_user(
    id: int,
    user: UserField,
    db: AsyncSession = Depends(get_db)
) -> UserResponse:
    adapter = AdapterUser(db)
    request = CreateUser(organization_id=user.organization_id,
                             email=user.email,
                             password_hash=user.password_hash,
                             first_name=user.first_name,
                             last_name=user.last_name,
                             role=user.role)
    result = await update_user_case(id, request, adapter)
    return to_response(UserResponse, result)
   

@router.delete("/{id}", status_code=status.HTTP_204_NO_CONTENT)
async def delete_user(id: int, db: AsyncSession = Depends(get_db)) -> None:
  adapter = AdapterUser(db)
  request = GetUser(id=id)
  
  return await remove_user_case(request, adapter)
