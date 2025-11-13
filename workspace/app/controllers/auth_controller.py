from fastapi import APIRouter, Depends, HTTPException, status
from app.schemas.user_schema import UserCreate
from app.services.auth_service import AuthService
from app.repositories.user_repository import UserRepository
from sqlalchemy.ext.asyncio import AsyncSession
from app.dependencies import get_db
from fastapi.security import OAuth2PasswordRequestForm

router = APIRouter(prefix='/auth', tags=['auth'])

@router.post('/login')
async def login(
    form_data: OAuth2PasswordRequestForm = Depends(),
    db: AsyncSession = Depends(get_db)
):
    user_repo = UserRepository(db)
    user = await user_repo.get_by_username(form_data.username)
    if not user or not AuthService.verify_password(form_data.password, user.password_hash):
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="Invalid credentials")
    access_token = AuthService.create_access_token(str(user.id))
    return {"access_token": access_token, "token_type": "bearer"}
