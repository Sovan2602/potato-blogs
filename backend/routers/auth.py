from fastapi import APIRouter, Depends, HTTPException, status, BackgroundTasks
from sqlalchemy.orm import Session
from fastapi.security import OAuth2PasswordRequestForm
from backend.login import schemas,crud,utils,auth

router = APIRouter(
    prefix="/auth",
    tags=["auth"]
)

@router.post("/token", response_model=schemas.Token)
async def login_for_access_token(form_data: OAuth2PasswordRequestForm = Depends(), db: Session = Depends(utils.get_db)):
    user = auth.authenticate_user(db, form_data.username, form_data.password)
    if not user:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Incorrect email or password",
            headers={"WWW-Authenticate": "Bearer"},
        )
    access_token_expires = timedelta(minutes=settings.ACCESS_TOKEN_EXPIRE_MINUTES)
    access_token = auth.create_access_token(
        data={"sub": user.email}, expires_delta=access_token_expires
    )
    return {"access_token": access_token, "token_type": "bearer"}

@router.post("/password-reset/")
async def password_reset(request: schemas.PasswordReset, db: Session = Depends(utils.get_db)):
    user = crud.get_user_by_email(db, email=request.email)
    if not user:
        raise HTTPException(status_code=404, detail="User not found")
    token = utils.create_reset_token(email=user.email)
    # Replace this line with sending email functionality
    print(f"Use this token to reset your password: {token}")
    return {"message": "Password reset token sent"}

@router.post("/reset-password/", response_model=schemas.User)
async def reset_password(request: schemas.ResetPassword, db: Session = Depends(utils.get_db)):
    user = crud.get_user_by_email(db, email=request.email)
    if not user:
        raise HTTPException(status_code=404, detail="User not found")
    return crud.update_user_password(db, user, request.new_password)

@router.post("/users/", response_model=schemas.User)
async def create_user(user: schemas.UserCreate, db: Session = Depends(utils.get_db)):
    db_user = crud.get_user_by_email(db, email=user.email)
    if db_user:
        raise HTTPException(status_code=400, detail="Email already registered")
    return crud.create_user(db=db, user=user)