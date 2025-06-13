# هذا الملف يعرف جدول الربط many-to-many بين المستخدمين والأدوار (UserRole) مع ضمان عدم وجود تكرار للعلاقات
from sqlalchemy import (
    Column,
    Integer,
    ForeignKey,
    UniqueConstraint,
)  # استيراد أعمدة وأنواع البيانات من SQLAlchemy مع دعم المفتاح الأجنبي وفرض التقييدات الفريدة
from app.db.database import (
    Base,
)  # استيراد القاعدة الأساسية للنماذج من ملف قاعدة البيانات


class UserRole(Base):
    __tablename__ = "user_roles"  # اسم الجدول في قاعدة البيانات
    __table_args__ = (
        UniqueConstraint("user_id", "role_id"),
    )  # ضمان عدم تكرار نفس زوج المستخدم والدور في الجدول

    id = Column(
        Integer, primary_key=True, index=True
    )  # معرف فريد لكل سجل في الجدول مع فهرسة لتحسين الأداء
    user_id = Column(
        Integer, ForeignKey("users.id")
    )  # عمود يمثل المفتاح الأجنبي لمعرف المستخدم في جدول users
    role_id = Column(
        Integer, ForeignKey("roles.id")
    )  # عمود يمثل المفتاح الأجنبي لمعرف الدور في جدول roles


