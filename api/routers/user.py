from typing import List
from fastapi import APIRouter, HTTPException, status, Depends
from sqlalchemy import select
from sqlalchemy.exc import IntegrityError
from sqlalchemy.ext.asyncio import AsyncSession
from schemas.user import UserField, UserResponse
from db.Session import get_db
from models.user import User
from models.organization import Organization

user_router = APIRouter(tags=["users"])

@user_router.get("/", response_model=List[UserResponse])
async def get_users(db: AsyncSession = Depends(get_db)) -> List[dict]:
  query = select(User)
  result = await db.execute(query)
  return result.scalars().all()

@user_router.get("/{id}", response_model=UserResponse)
async def get_user(id: int, db: AsyncSession = Depends(get_db)) -> dict:
  query = select(User).where(User.id == id)
  result = await db.execute(query)
  user = result.scalars().first()

  if not user:
    raise HTTPException(status_code=status.HTTP_404_NOT_FOUND)
  
  return user

@user_router.post(
  "/",
  response_model=UserResponse,
  status_code=status.HTTP_201_CREATED
)
async def create_user(user: UserField, db: AsyncSession = Depends(get_db)) -> dict:

  query_email = select(User.email).where(User.email == user.email)
  result_email = await db.execute(query_email)
  db_email = result_email.scalar_one_or_none()

  if db_email:
    raise  HTTPException(
	status_code=status.HTTP_409_CONFLICT,
	detail=f"Email: {user.email} already exists!"
	)

  query_org = select(Organization.id).where(Organization.id == user.organization_id)
  result_org = await db.execute(query_org)
  db_org = result_org.scalar_one_or_none()

  if not db_org:
    raise HTTPException(
	status_code=status.HTTP_404_NOT_FOUND,
	detail=f"Organization ID: {user.organization_id} not found"
	)

  new_user = User(**user.model_dump())
  db.add(new_user)
  await db.commit()
  await db.refresh(new_user)
  return new_user

@user_router.put("/{id}", response_model=UserResponse)
async def update_user(
    id: int,
    user: UserField,
    db: AsyncSession = Depends(get_db)
) -> User:

  db_user = await db.get(User, id)
  if not db_user:
    raise HTTPException(
	status_code=status.HTTP_404_NOT_FOUND, 
        detail=f"User with ID {id} not found"
      )

  data = user.model_dump(exclude_unset=True)
  for field, value in data.items():
    setattr(db_user, field, value)

  try:
    await db.commit()
    await db.refresh(db_user)
    return db_user
  except IntegrityError as e:
     await db.rollback()
     err_msg = str(e.orig).lower()

     if "email" in err_msg:
       raise HTTPException(
		 status_code=status.HTTP_409_CONFLICT,
		 detail=f"Email '{user.email}' already exists."
	)
     if "organization" in err_msg:
        raise HTTPException(
		status_code=status.HTTP_404_NOT_FOUND,
		detail=f"Organization ID '{user.organization_id}' not found."
	)
     raise HTTPException(
	status_code=status.HTTP_400_BAD_REQUEST,
	detail="Database integrity constraint violation."
	)

@user_router.delete("/{id}", status_code=status.HTTP_204_NO_CONTENT)
async def delete_user(id: int, db: AsyncSession = Depends(get_db)) -> None:
  query = select(User).where(User.id == id)
  result = await db.execute(query)
  user = result.scalars().first()

  if not user:
    raise HTTPException(status_code=status.HTTP_404_NOT_FOUND)

  await db.delete(user)
  await db.commit()
  return None
