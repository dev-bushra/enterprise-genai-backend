# إضافة كود التحقق من التوكن JWT وAuth Middleware
"""
شرح عام:
oauth2_scheme يهيئ سير العمل الخاص بـ OAuth2 مع Azure AD عن طريق عنوان الدخول وتبادل التوكن.
get_current_user هي دالة تعتمد على التوكن المرسل في الهيدر (Authorization).
تستخدم Security(oauth2_scheme) لجلب التوكن من طلب المستخدم والتحقق المبدئي.
ثم تمرر التوكن إلى decode_token (التي شرحناها سابقًا) للتحقق الكامل وفك التوكن.
في النهاية ترجع بيانات المستخدم المستخرجة من التوكن.

# ملخص الملف:
# هذا الملف يعرّف أداة OAuth2 لاستخدام Google Authorization Code Flow، ويوفر دالة تعتمد على توكن JWT المرسل
# لتفكيكه والتحقق من صحته عن طريق Google، ثم تعيد بيانات المستخدم المصادق عليه.
"""

from fastapi import (
    Depends,
    Security,
)  # استيراد Depends و Security لإدارة الاعتماديات الأمنية في FastAPI
from fastapi.security import (
    OAuth2AuthorizationCodeBearer,
)  # استيراد أداة OAuth2 Authorization Code Bearer لتطبيق OAuth2 Authorization Code Flow
from app.core.config import (
    settings,
)  # استيراد إعدادات التطبيق (مثلاً client_id وغيره لو تستخدم في مكان آخر)
from app.auth.google_validator import (
    decode_google_token,
)  # استيراد دالة فك التوكن والتحقق من صحته من Google


oauth2_scheme = OAuth2AuthorizationCodeBearer(
    authorizationUrl="https://accounts.google.com/o/oauth2/v2/auth",  # رابط دخول المستخدم لتسجيل الدخول عبر Google OAuth2
    tokenUrl="https://oauth2.googleapis.com/token",  # رابط تبادل كود التفويض (authorization code) بتوكن وصول من Google
)


async def get_current_user(token: str = Security(oauth2_scheme)):
    return await decode_google_token(
        token
    )  # فك التوكن JWT والتحقق من صحته وإرجاع بيانات المستخدم المصدق عليه
