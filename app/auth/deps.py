# Dependency للتحقق من صلاحيات المستخدم
# هذا الملف يُعرف دالة لتقييد الوصول حسب الأدوار باستخدام Dependency Injection مع التحقق من توكن المستخدم وأدواره من قاعدة البيانات.

from fastapi import (
    Depends,
    HTTPException,
    status,
)  # استيراد أدوات حقن الاعتمادية واستثناءات HTTP من FastAPI
from app.auth.oauth2 import (
    get_current_user,
)  # دالة للحصول على المستخدم الحالي بعد التحقق من التوكن
from app.auth.rbac import (
    get_user_roles,
)  # دالة لاسترجاع أدوار المستخدم من قاعدة البيانات
from app.db.database import (
    get_db,
)  # دالة للحصول على جلسة قاعدة البيانات (Dependency Injection)
from sqlalchemy.ext.asyncio import (
    AsyncSession,
)  # نوع الجلسة غير المتزامنة لـ SQLAlchemy


async def require_roles(
    allowed_roles: list[str],
):  # دالة تأخذ قائمة بالأدوار المسموح بها (مثلاً ["admin", "editor"])
    async def _check_roles(  # دالة داخلية تستخدم في Dependency Injection للتحقق من صلاحيات المستخدم
        current_user: dict = Depends(
            get_current_user
        ),  # المستخدم الحالي مستخرج من التوكن
        db: AsyncSession = Depends(get_db),  # جلسة قاعدة بيانات غير متزامنة
    ):
        user_id = current_user.get(
            "sub"
        )  # الحصول على معرف المستخدم من بيانات التوكن (عادة يكون "sub")
        roles = await get_user_roles(
            user_id, db
        )  # استرجاع أدوار المستخدم من قاعدة البيانات

        if not any(
            role in allowed_roles for role in roles
        ):  # التحقق هل المستخدم لديه أي دور من الأدوار المسموح بها
            raise HTTPException(
                status_code=status.HTTP_403_FORBIDDEN,  # إذا لا، رد 403 ممنوع الوصول
                detail="Access denied",
            )
        return current_user  # إذا تمت الموافقة، ترجع بيانات المستخدم

    return _check_roles  # ترجع دالة التحقق لاستخدامها كـ Dependency في الراوتات


