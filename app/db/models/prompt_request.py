# 🔚 هذا الملف يُعرّف جدول الطلبات (PromptRequest) في قاعدة البيانات، ويستخدم enum للحالة،
# ويتضمن علاقة 1:1 مع جدول الردود المرتبطة بالذكاء الاصطناعي.

from sqlalchemy import (
    Column,
    String,
    Text,
    DateTime,
    Enum,
    ForeignKey,
)  # استيراد أعمدة SQL الأساسية
from sqlalchemy.dialects.postgresql import UUID  # دعم UUID لقاعدة PostgreSQL
from sqlalchemy.orm import relationship  # لإدارة العلاقات بين الجداول
from datetime import datetime  # لجلب الوقت الحالي
import uuid  # لإنشاء معرفات UUID فريدة
import enum  # لإنشاء تعداد ثابت لقيم الحالة

from app.db.database import Base  # استيراد Base لتعريف الموديل


class PromptStatus(str, enum.Enum):  # تعريف enum يمثل حالات الطلب المختلفة
    pending = "pending"  # الطلب قيد الانتظار
    processing = "processing"  # الطلب يتم معالجته
    completed = "completed"  # تم توليد الرد
    failed = "failed"  # حدث خطأ أثناء التوليد


class PromptRequest(Base):  # تعريف جدول الطلبات في قاعدة البيانات
    __tablename__ = "prompt_requests"  # اسم الجدول في قاعدة البيانات

    id = Column(
        UUID(as_uuid=True), primary_key=True, default=uuid.uuid4
    )  # معرف فريد للطلب
    user_id = Column(
        UUID(as_uuid=True), ForeignKey("users.id"), nullable=False
    )  # مرجع للمستخدم الذي أرسل الطلب
    model = Column(
        String, nullable=False
    )  # اسم نموذج الذكاء الاصطناعي المستخدم (مثلاً gpt-4)
    prompt_type = Column(String, nullable=True)  # نوع الطلب (مثلاً: نصي، كود، تحليل، ..)
    prompt_text = Column(Text, nullable=False)  # نص الطلب المُرسل إلى الذكاء الاصطناعي
    status = Column(
        Enum(PromptStatus), default=PromptStatus.pending
    )  # الحالة الحالية للطلب
    created_at = Column(DateTime, default=datetime.utcnow)  # وقت إرسال الطلب

    response = relationship(
        "PromptResponse", back_populates="prompt", uselist=False
    )  # علاقة 1:1 مع جدول الرد


