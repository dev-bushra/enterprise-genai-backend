# ملخص الملف:
# هذا الملف يُعرّف إعدادات التطبيق الأساسية باستخدام Pydantic BaseSettings لقراءة متغيرات البيئة بطريقة آمنة ومرنة. يحتوي على إعدادات خاصة بالمصادقة مثل معرف التينانت في Azure، ومعرف وسر تطبيق Google، مع خصائص للتحقق من JWT مثل الجمهور والخوارزمية.
# كائن settings يُستخدم في باقي المشروع للوصول إلى هذه القيم بسهولة دون تكرار الكود أو الكتابة الصلبة (hardcoding).

from pydantic import (
    BaseSettings,
)  # تستورد BaseSettings لإدارة الإعدادات من متغيرات البيئة بشكل آمن وذكي


class Settings(
    BaseSettings
):  # تعريف كلاس Settings يرث من BaseSettings لجلب القيم من .env أو النظام
    AZURE_TENANT_ID: str  # معرف التينانت في Azure - مطلوب للمصادقة
    GOOGLE_CLIENT_ID: str  # معرف التطبيق (Client ID) في Azure - يحدد التطبيق
    GOOGLE_CLIENT_SECRET: str  # سر التطبيق (Client Secret) - يستخدم للمصادقة الآمنة
    AZURE_AUTHORITY: str = (
        "https://login.microsoftonline.com"  # عنوان المصادقة الرئيسي في Azure - قيمة افتراضية
    )
    API_AUDIENCE: str  # الـ App ID URI الذي يستخدم للتحقق من صحة JWT - مهم جداً
    ALGORITHM: str = "RS256"  # خوارزمية التوقيع المستخدمة للتحقق من JWT - عادة RS256

    class Config:  # كلاس داخلي لتحديد إعدادات خاصة بالـ Pydantic
        env_file = ".env"  # يحدد أن القيم ستُقرأ من ملف .env في الجذر


settings = Settings()  # ينشئ كائن settings بتحميل القيم من .env أو من بيئة النظام
