# ✅ ملخص الملف user.py:
# هذا الملف يعرف نموذج ORM باسم User يمثل جدول المستخدمين في قاعدة البيانات.
# يتضمن الحقول الأساسية: id، email، full_name، حالة التفعيل، نوع المستخدم (مشرف أم لا)، وتاريخ الإنشاء.
# هذا النموذج يستخدمه SQLAlchemy لإنشاء وإدارة الجدول "users" تلقائيًا في قاعدة البيانات باستخدام الميثاق البرمجي Base.


from sqlalchemy import (
    Column,
    String,
    Boolean,
    Integer,
    DateTime,
)  # استيراد أنواع الأعمدة المطلوبة من SQLAlchemy
from app.db.database import Base  # استيراد الـ Base class لتعريف النموذج ORM
from datetime import datetime  # استيراد datetime لتعيين وقت الإنشاء التلقائي


class User(Base):  # تعريف كلاس ORM يمثل جدول "users" في قاعدة البيانات
    __tablename__ = "users"  # اسم الجدول في قاعدة البيانات سيكون "users"

    id = Column(
        Integer, primary_key=True, index=True
    )  # عمود ID (مفتاح أساسي) مع index لتحسين الأداء
    email = Column(
        String, unique=True, index=True, nullable=False
    )  # بريد إلكتروني فريد مطلوب مع index
    full_name = Column(String, nullable=True)  # اسم المستخدم الكامل (اختياري)
    is_active = Column(Boolean, default=True)  # حالة تفعيل الحساب (افتراضي مفعّل)
    is_superuser = Column(Boolean, default=False)  # هل المستخدم مشرف؟ (افتراضي: لا)
    created_at = Column(
        DateTime, default=datetime.utcnow
    )  # وقت إنشاء الحساب (تلقائي عند الإنشاء)

roles = relationship("UserRole", backref="user")
