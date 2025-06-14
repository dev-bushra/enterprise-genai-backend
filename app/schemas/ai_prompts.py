# 🧠 هذا الملف يحتوي على ثلاث مخططات بيانات (Schemas):
# 1. PromptCreate ➜ يُستخدم عند إرسال طلب جديد للذكاء الاصطناعي.
# 2. PromptOut ➜ يُستخدم عند عرض قائمة الطلبات بدون الردود.
# 3. PromptDetail ➜ يُستخدم عند عرض التفاصيل الكاملة لطلب، مع الرد والمدة.
# هذه المخططات تُستخدم لضمان التحقق من صحة البيانات (validation) بين الواجهة الأمامية والـ API.
# 📁 المسار: app/schemas/ai_prompts.py

from pydantic import BaseModel  # استيراد BaseModel من Pydantic لتعريف المخططات
from uuid import UUID  # لتحديد الحقول من نوع UUID
from datetime import datetime  # لتحديد الحقول الزمنية
from typing import Optional  # للتعامل مع الحقول الاختيارية

from app.db.models.prompt_request import PromptStatus  # استيراد Enum الخاص بحالة الطلب


# 🔹 البيانات المطلوبة لإنشاء طلب جديد [عند إنشاء طلب جديد (POST)]
# Prompt Create
class PromptCreate(BaseModel):
    model: str  # اسم نموذج الذكاء الاصطناعي (مثلاً: gpt-4)
    prompt_type: Optional[str] = None  # نوع المحتوى (نص، كود، تحليل...) - اختياري
    prompt_text: str  # النص المُرسل إلى الذكاء الاصطناعي


# 🔹 البيانات التي نُرجعها عند عرض الطلبات بدون الرد [عند عرض قائمة الطلبات (GET /)]
# Prompt Out
class PromptOut(BaseModel):
    id: UUID  # معرف الطلب
    model: str  # اسم النموذج المستخدم
    prompt_type: Optional[str] = None  # نوع الطلب - اختياري
    status: PromptStatus  # الحالة الحالية للطلب (pending، processing، ...)
    created_at: datetime  # وقت إنشاء الطلب

    class Config:
        orm_mode = True  # لتفعيل التحويل من ORM (SQLAlchemy model) إلى Pydantic


# 🔹 البيانات مع الرد الكامل من الذكاء الاصطناعي [	عند عرض طلب مفرد (GET /{id}) ]
# Prompt Detail
class PromptDetail(PromptOut):  # يرث الحقول العامة من PromptOut
    prompt_text: str  # النص الأصلي المرسل
    response_text: Optional[str] = None  # الرد من الذكاء الاصطناعي - اختياري
    duration_ms: Optional[int] = None  # الوقت المستغرق في توليد الرد - اختياري
