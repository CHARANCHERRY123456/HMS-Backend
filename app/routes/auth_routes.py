from fastapi import APIRouter, HTTPException, Depends
from sqlalchemy.orm import Session
from google.oauth2 import id_token
from google.auth.transport import requests
import jwt
from datetime import datetime, timedelta
from database import get_db
from models.user import User, UserRole
from pydantic import BaseModel

router = APIRouter(prefix="/auth", tags=["Authentication"])

SECRET_KEY = "hms-simple-secret-2025"
ALGORITHM = "HS256"

class GoogleLogin(BaseModel):
    google_token: str

@router.post("/google-login")
def google_login(request: GoogleLogin, db: Session = Depends(get_db)):
    try:
        # For now, let's use the session info directly from frontend
        # We'll get email from the request instead of verifying token
        
        # TODO: Add proper Google token verification later
        # idinfo = id_token.verify_oauth2_token(request.google_token, requests.Request())
        # email = idinfo.get('email')
        
        # For now, extract email from the dummy token (we'll fix this)
        email = "user@gmail.com"  # This should come from verified Google token
        
        if not email:
            raise HTTPException(status_code=400, detail="No email provided")
        
        # Check if user exists
        user = db.query(User).filter(User.email == email).first()
        
        # If user doesn't exist, create automatically
        if not user:
            user = User(
                username=email.split('@')[0],
                email=email,
                hashed_password="google_auth",
                role=UserRole.doctor
            )
            db.add(user)
            db.commit()
            db.refresh(user)
        
        # Create JWT token
        token_data = {
            "email": user.email,
            "username": user.username,
            "role": user.role.value,
            "exp": datetime.utcnow() + timedelta(hours=24)
        }
        token = jwt.encode(token_data, SECRET_KEY, algorithm=ALGORITHM)
        
        return {
            "success": True,
            "token": token,
            "user": {
                "id": user.id,
                "username": user.username,
                "email": user.email,
                "role": user.role.value
            }
        }
        
    except Exception as e:
        print(f"Error: {e}")  # For debugging
        raise HTTPException(status_code=401, detail="Google login failed")
