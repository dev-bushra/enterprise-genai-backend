# دالة Helper لجلب أدوار المستخدم
# هذا الملف يوفر دالة للحصول على أدوار المستخدم حسب الـ user_id عبر جلسة قاعدة بيانات غير متزامنة.

from sqlalchemy.ext.asyncio import (
    AsyncSession,
)  # استيراد جلسة قاعدة بيانات غير متزامنة من SQLAlchemy
from sqlalchemy.future import select  # استيراد دالة select الحديثة لبناء استعلامات SQL
from app.db.models.user_role import (
    UserRole,
)  # استيراد نموذج جدول user_roles لربط المستخدمين بالأدوار
from app.db.models.role import Role  # استيراد نموذج جدول roles لتعريف الأدوار


async def get_user_roles(
    user_id: int, db: AsyncSession
):  # دالة غير متزامنة لاسترجاع أدوار المستخدم من قاعدة البيانات
    result = await db.execute(
        select(Role.name)
        .join(UserRole)
        .where(
            UserRole.user_id == user_id
        )  # استعلام لجلب أسماء الأدوار المرتبطة بالمستخدم
    )
    return [
        r[0] for r in result.fetchall()
    ]  # ترجع قائمة بأسماء الأدوار مثل ["admin", "viewer"]


