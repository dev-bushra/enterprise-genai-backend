# ملخص الملف:
# هذا الملف مسؤول عن تحميل مفاتيح JWKS الخاصة بجوجل، واستخدامها للتحقق من صحة JWT التي يصدرها Google Identity.
# يشمل ذلك فك التوكن، التحقق من التوقيع، التحقق من الجمهور (audience)، ومن جهة الإصدار (issuer).
# في حالة نجاح التحقق، تُرجع بيانات المستخدم المستخرجة من التوكن.

from jose import (
    jwt,
    JWTError,
)  # استيراد مكتبة jwt لفك التوكن والتعامل مع الأخطاء الخاصة به
from fastapi import (
    HTTPException,
    status,
)  # استيراد استثناء HTTP لاستخدامه في ردود الخطأ
import httpx  # استيراد مكتبة httpx لإرسال طلبات HTTP بشكل غير متزامن
from app.core.config import settings  # استيراد إعدادات المشروع من ملف الكونفيج

JWKS_URL = "https://www.googleapis.com/oauth2/v3/certs"  # رابط الحصول على مفاتيح JWKS من جوجل للتحقق من التوقيع
ISSUER = "https://accounts.google.com"  # الجهة المصدرة للتوكن (مُعرف موثوق لجوجل)

_jwks_cache = {}  # كاش مؤقت لتخزين مفاتيح JWKS لمنع الطلبات المتكررة الزائدة


async def get_google_jwks():  # دالة للحصول على مفاتيح JWKS من جوجل بشكل غير متزامن
    global _jwks_cache  # استخدام المتغير العالمي للكاش
    if not _jwks_cache:  # إذا لم يكن الكاش مملوءًا (أول طلب)
        async with httpx.AsyncClient() as client:  # فتح عميل HTTP غير متزامن
            res = await client.get(JWKS_URL)  # إرسال طلب GET لجلب مفاتيح JWKS من جوجل
            _jwks_cache = res.json()  # تخزين المفاتيح في الكاش بصيغة JSON
    return _jwks_cache  # إرجاع المفاتيح المخزنة (إما من الكاش أو من الطلب الجديد)


async def decode_google_token(token: str):  # دالة لفك والتحقق من JWT الخاص بجوجل
    try:
        unverified_header = jwt.get_unverified_header(
            token
        )  # قراءة الهيدر من التوكن بدون تحقق كامل (للحصول على kid)
    except JWTError:
        raise HTTPException(
            status_code=401, detail="Invalid JWT header"
        )  # خطأ 401 لو الهيدر غير صالح

    jwks = await get_google_jwks()  # الحصول على مفاتيح JWKS من جوجل (من الكاش أو جديد)

    for key in jwks["keys"]:  # البحث داخل مفاتيح JWKS عن المفتاح المناسب
        if key["kid"] == unverified_header["kid"]:  # المطابقة حسب kid من الهيدر
            public_key = jwt.construct_rsa_public_key(
                key
            )  # بناء المفتاح العام من بيانات JWKS
            try:
                payload = jwt.decode(  # فك التوكن والتحقق من صحته وتوقيعه
                    token,
                    public_key,
                    algorithms=["RS256"],  # خوارزمية التوقيع المتوقعة من جوجل
                    audience=settings.GOOGLE_CLIENT_ID,  # التحقق من أن التوكن موجّه للتطبيق الخاص (client_id)
                    issuer=ISSUER,  # التحقق من جهة الإصدار (جوجل)
                )
                return payload  # إرجاع بيانات المستخدم (payload) بعد التحقق الكامل
            except JWTError as e:
                raise HTTPException(  # في حال فشل التحقق، إرجاع خطأ مع رسالة مفصلة
                    status_code=401, detail=f"Token validation error: {e}"
                )

    raise HTTPException(
        status_code=401, detail="Unable to find matching key in JWKS"
    )  # خطأ لو لم يتم إيجاد المفتاح المناسب في JWKS
