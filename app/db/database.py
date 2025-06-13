# ملخص الملف:
# ملف إعداد قاعدة البيانات باستخدام SQLAlchemy مع دعم العمليات غير المتزامنة (async).
# يُنشئ محرك اتصال بقاعدة بيانات PostgreSQL أو أي قاعدة أخرى عبر رابط اتصال من الإعدادات، ويجهز جلسة async تستخدم عبر Dependency Injection في نقاط النهاية داخل التطبيق.
# أيضًا يحتوي على القاعدة الأساسية لتعريف نماذج ORM.

from sqlalchemy.ext.asyncio import (
    create_async_engine,
    AsyncSession,
)  # استيراد لإنشاء محرك async وجلسة async لـ SQLAlchemy
from sqlalchemy.orm import (
    sessionmaker,
    declarative_base,
)  # استيراد لإنشاء session factory و base class للنماذج
from app.core.config import (
    settings,
)  # استيراد إعدادات المشروع (مثل رابط قاعدة البيانات)

# رابط الاتصال بقاعدة البيانات (مثال: postgresql+asyncpg://user:password@localhost/dbname)
DATABASE_URL = (
    settings.DATABASE_URL
)  

# إنشاء محرك قاعدة بيانات غير متزامن مع تمكين عرض SQL في اللوج
engine = create_async_engine(
    DATABASE_URL, echo=True
) 

# إنشاء مصنع لجلسات async ترتبط بمحرك قاعدة البيانات
AsyncSessionLocal = sessionmaker(  
    bind=engine,
    class_=AsyncSession,  # استخدام جلسة غير متزامنة
    expire_on_commit=False,  # منع انتهاء صلاحية الكائنات بعد commit لتجنب إعادة تحميلها
)

# إنشاء القاعدة الأساسية لتعريف نماذج ORM (تعريف الجداول)
Base = declarative_base()  


# دالة Dependency Injection للحصول على جلسة DB غير متزامنة عند الحاجة
async def get_db():
    async with AsyncSessionLocal() as session:  # إنشاء جلسة جديدة async مع إدارة الموارد
        yield session  # تسليم الجلسة للاستخدام في نقطة النهاية ثم إغلاقها تلقائياً
