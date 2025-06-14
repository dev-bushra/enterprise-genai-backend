# 🔚 هذا الملف يعرّف جدول الردود (PromptResponse) في قاعدة البيانات، ويمثل استجابة الذكاء الاصطناعي
# المرتبطة مباشرة بكل طلب من المستخدم (علاقة 1:1 مع PromptRequest).

from sqlalchemy import (
    Column,
    Text,
    DateTime,
    ForeignKey,
    Integer,
)  # استيراد أنواع الأعمدة المطلوبة
from sqlalchemy.dialects.postgresql import UUID  # دعم UUID في PostgreSQL
from sqlalchemy.orm import relationship  # لإدارة العلاقات بين الجداول
from datetime import datetime  # للحصول على الوقت الحالي
import uuid  # لإنشاء UUID فريد

from app.db.database import Base  # استيراد الـ Base لتعريف النموذج


class PromptResponse(Base):  # تعريف كلاس يمثل جدول ردود الذكاء الاصطناعي
    __tablename__ = "prompt_responses"  # اسم الجدول في قاعدة البيانات

    id = Column(
        UUID(as_uuid=True), primary_key=True, default=uuid.uuid4
    )  # معرف فريد للرد
    prompt_id = Column(
        UUID(as_uuid=True),
        ForeignKey("prompt_requests.id"),
        nullable=False,
        unique=True,
    )  # ارتباط بـ PromptRequest (علاقة 1:1)
    response_text = Column(Text, nullable=True)  # نص الرد المُولد من الذكاء الاصطناعي
    duration_ms = Column(Integer, nullable=True)  # مدة التوليد بالمللي ثانية
    created_at = Column(DateTime, default=datetime.utcnow)  # وقت إنشاء الرد

    prompt = relationship(
        "PromptRequest", back_populates="response"
    )  # الربط العكسي مع الطلب الأصلي


