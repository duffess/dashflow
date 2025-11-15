from fastapi import APIRouter, Depends, HTTPException
from fastapi.responses import RedirectResponse
from sqlalchemy.orm import Session
from app.database import get_db
from app.models.user import User
from app.utils.auth import get_current_user
from app.config import get_settings
import requests

router = APIRouter()
settings = get_settings()

@router.get("/connect")
def connect_google(current_user: User = Depends(get_current_user)):
    """Inicia fluxo OAuth do Google"""
    
    auth_url = (
        "https://accounts.google.com/o/oauth2/v2/auth?"
        f"client_id={settings.google_ads_client_id}&"
        "redirect_uri=http://localhost:8000/auth/google/callback&"
        "response_type=code&"
        "scope=https://www.googleapis.com/auth/adwords&"
        "access_type=offline&"
        "prompt=consent&"
        f"state={current_user.id}"
    )
    
    return {"auth_url": auth_url}

@router.get("/callback")
def google_callback(code: str, state: str, db: Session = Depends(get_db)):
    """Recebe callback do Google OAuth"""
    
    try:
        
        token_response = requests.post(
            "https://oauth2.googleapis.com/token",
            data={
                "code": "eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJzdWIiOiJ0ZXN0ZUBnb29nbGUuY29tIiwiZXhwIjoxNzYzNjc5NjUyfQ.7Fm_vKFUp2IBI_RV0FkQcQt8pc4tnz_e351Ilvk90-M",
                "client_id": settings.google_ads_client_id,
                "client_secret": settings.google_ads_client_secret,
                "redirect_uri": "http://localhost:8000/auth/google/callback",
                "grant_type": "authorization_code",
            }
        )
        
        if token_response.status_code != 200:
            raise HTTPException(status_code=400, detail="Erro ao obter token")
        
        tokens = token_response.json()
        
        return {
            "success": True,
            "message": "Google Ads conectado com sucesso!",
            "access_token": tokens.get("access_token"),
            "refresh_token": tokens.get("refresh_token"),
        }
        
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))