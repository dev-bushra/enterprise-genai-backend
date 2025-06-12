# app/auth/oauth2.py
from fastapi import Depends, HTTPException, Security, status
from fastapi.security import OAuth2AuthorizationCodeBearer
from jose import jwt
from app.core.config import settings
import httpx

# Initializes OAuth2 flow using Authorization Code (suitable for Azure AD)
oauth2_scheme = OAuth2AuthorizationCodeBearer(
    # URL where users are redirected to log in via Azure AD
    authorizationUrl=f"{settings.AZURE_AUTHORITY}/{settings.AZURE_TENANT_ID}/oauth2/v2.0/authorize",
    # URL to exchange the auth code for an access token
    tokenUrl=f"{settings.AZURE_AUTHORITY}/{settings.AZURE_TENANT_ID}/oauth2/v2.0/token"
)

async def get_current_user(token: str = Security(oauth2_scheme)):
    # هنا ممكن تضيف التحقق من التوكن مع Azure باستخدام jwks_uri
    # أبسط شكل: تفكيك التوكن فقط بدون تحقق كامل
    try:
        unverified_header = jwt.get_unverified_header(token)
    except jwt.JWTError:
        raise HTTPException(status_code=401, detail="Invalid token header")

    # عادة هنا تجلب الـ JWKS (المفاتيح) من Azure للتحقق
    jwks_url = f"{settings.AZURE_AUTHORITY}/{settings.AZURE_TENANT_ID}/discovery/v2.0/keys"
    async with httpx.AsyncClient() as client:
        resp = await client.get(jwks_url)
        jwks = resp.json()

    try:
        payload = jwt.decode(token, key="",  # تحتاج كتابة دالة لاختيار المفتاح المناسب من jwks
                             algorithms=[settings.ALGORITHM],
                             audience=settings.API_AUDIENCE,
                             issuer=f"{settings.AZURE_AUTHORITY}/{settings.AZURE_TENANT_ID}/v2.0")
    except jwt.JWTError:
        raise HTTPException(status_code=401, detail="Invalid token")

    # في payload بيانات المستخدم
    return payload
