
# ============================================================
# 📄 SUMMARY:
# هذا الملف يعرّف جدول "roles" في قاعدة البيانات باستخدام SQLAlchemy.
# يحتوي كل دور (Role) على:
# - id: معرف رقمي أساسي
# - name: اسم الدور (فريد مثل "admin" أو "viewer")
# - description: وصف اختياري
# يُستخدم هذا الجدول لتطبيق نظام RBAC (التحكم في الصلاحيات حسب الدور).
# ============================================================


# app/db/models/role.py

from sqlalchemy import (
    Column,
    Integer,
    String,
)  # استيراد أنواع الأعمدة من SQLAlchemy (رقم صحيح، نص)
from app.db.database import Base  # استيراد الكلاس الأساسي Base لتعريف نماذج الجداول


class Role(Base):  # تعريف كلاس Role يمثل جدول "roles" في قاعدة البيانات
    __tablename__ = "roles"  # تحديد اسم الجدول الفعلي في قاعدة البيانات ليكون "roles"

    id = Column(
        Integer, primary_key=True, index=True
    )  # معرف فريد لكل دور (مفتاح رئيسي + مفهرس لتحسين الأداء)
    name = Column(
        String, unique=True, index=True
    )  # اسم الدور (مثل admin أو viewer)، يجب أن يكون فريدًا + مفهرس
    description = Column(
        String, nullable=True
    )  # وصف اختياري للدور لتوضيح صلاحياته أو وظيفته

