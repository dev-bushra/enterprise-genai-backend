# 🔐 الجزء المتقدّم: التحقق من JWT باستخدام مفاتيح JWKS

"""
شرح عام:
هذه الوحدة مسؤولة عن جلب مفاتيح JWKS من Azure بشكل مؤقت (كاش) لتقليل الطلبات.
تستخدم بيانات رأس JWT (kid) لتحديد المفتاح المناسب للتحقق من التوقيع.
ثم تتحقق من صحة التوكن (التحقق من التوقيع، الجمهور، المصدر).
في حال وجود أي خطأ في التوكن أو المفتاح، ترجع خطأ HTTP 401 مع رسالة واضحة.

# ملخص الملف:
# هذا الملف مسؤول عن جلب مفاتيح JWKS الخاصة بـ Azure AD، والتحقق من صحة JWT Access Tokens.
# يتم فك التوكن، التحقق من التوقيع، الجمهور، والمصدر، ثم إعادة بيانات المستخدم بعد التحقق الكامل.
"""

from jose import jwt, JWTError  # استيراد مكتبة jose لفك وترميز JWT والتعامل مع الأخطاء
from fastapi import (
    HTTPException,
    status,
)  # استيراد استثناء HTTP وأكواد الحالة من FastAPI
import httpx  # استيراد مكتبة httpx لإجراء طلبات HTTP غير متزامنة
from app.core.config import settings  # استيراد الإعدادات الخاصة بالتطبيق


# متغير لتخزين مفاتيح JWKS مؤقتاً لتقليل الطلبات المتكررة للخادم
_jwks_cache = {}  # تخزين مؤقت للمفاتيح


async def get_jwks():
    global _jwks_cache  # استخدام المتغير العام
    if not _jwks_cache:  # إذا لم تكن المفاتيح مخزنة مسبقاً
        url = f"{settings.AZURE_AUTHORITY}/{settings.AZURE_TENANT_ID}/discovery/v2.0/keys"  # عنوان JWKS في Azure
        async with httpx.AsyncClient() as client:
            res = await client.get(url)  # جلب المفاتيح من سيرفر Azure بشكل غير متزامن
            _jwks_cache = res.json()  # تخزين المفاتيح المستلمة في الذاكرة المؤقتة
    return _jwks_cache  # إرجاع المفاتيح


async def decode_token(token: str):
    try:
        unverified_header = jwt.get_unverified_header(
            token
        )  # استخراج رأس التوكن بدون تحقق (للحصول على kid)
    except JWTError:
        raise HTTPException(
            status_code=401, detail="Invalid JWT header"
        )  # رفض التوكن إذا الرأس غير صحيح

    jwks = await get_jwks()  # جلب مفاتيح JWKS (مخزنة أو جديدة)

    # البحث عن المفتاح المناسب حسب kid في رأس التوكن
    for key in jwks["keys"]:
        if key["kid"] == unverified_header["kid"]:  # مطابقة معرف المفتاح (kid)
            public_key = jwt.construct_rsa_public_key(
                key
            )  # بناء المفتاح العمومي من بيانات JWKS
            try:
                payload = jwt.decode(
                    token,
                    public_key,  # المفتاح العمومي للتحقق من التوقيع
                    algorithms=[settings.ALGORITHM],  # خوارزمية التوقيع المتوقعة
                    audience=settings.API_AUDIENCE,  # الجمهور المسموح به (API الخاص بك)
                    issuer=f"{settings.AZURE_AUTHORITY}/{settings.AZURE_TENANT_ID}/v2.0",  # المصدر الموثوق من التوكن
                )
                return payload  # إذا التحقق ناجح، ترجع بيانات المستخدم
            except JWTError as e:
                raise HTTPException(
                    status_code=401, detail=f"Token validation error: {e}"
                )  # خطأ في التحقق

    # إذا لم يعثر على مفتاح مطابق في JWKS
    raise HTTPException(status_code=401, detail="Unable to find matching key in JWKS")
