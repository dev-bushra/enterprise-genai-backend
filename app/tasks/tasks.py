# استخدام RBAC داخل API
# هذا الملف يحتوي راوتر API مع راوتات محمية باستخدام نظام RBAC للتحقق من صلاحيات المستخدم قبل السماح بالدخول.

from fastapi import (
    APIRouter,
    Depends,
)  # استيراد APIRouter لإنشاء مجموعة من الراوتات و Depends لإدارة الاعتمادية
from app.auth.deps import require_roles  # استيراد دالة تحقق الأدوار (RBAC) من auth.deps

router = APIRouter()  # إنشاء راوتر مستقل لتجميع راوتات المهام


@router.get("/admin-only")  # راوت GET محمي، متاح فقط للمديرين
async def admin_data(
    user=Depends(require_roles(["admin"])),
):  # يحقن بيانات المستخدم بعد التحقق من دوره "admin"
    return {"msg": "هذا محتوى خاص بالمديرين فقط!"}  # رد بسيط يؤكد صلاحية الدخول


@router.get("/viewer-or-admin")  # راوت GET متاح للمديرين أو المشاهدين فقط
async def open_data(
    user=Depends(require_roles(["admin", "viewer"]))
):  # يحقن المستخدم بعد التأكد من الدور المناسب
    return {
        "msg": "أنت لديك صلاحية المشاهدة أو الإدارة 👀"
    }  # رد بسيط يوضح الوصول المسموح
