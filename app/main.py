"""
شرح مبسط واحترافي:
Depends هو أداة من FastAPI تستخدم لإدارة الاعتمادات (Dependency Injection) مثل التحقق من المستخدم أو قواعد البيانات أو إعدادات أخرى.
get_current_user هي دالة تحقق من هوية المستخدم الحالي (مثلاً بالتحقق من التوكن JWT) وتعيد معلومات المستخدم.
عندما تنادي الـ endpoint /profile، FastAPI تلقائيًا يستدعي get_current_user ويربط النتيجة بالمعامل user.
النتيجة تكون بيانات المستخدم موجودة داخل user، وتُعاد في رد الـ API على شكل JSON.

# ملخص الملف:
# يحتوي على نقطة نهاية API تسمح للعملاء بالحصول على بيانات المستخدم الحالي بعد التحقق من هوية المستخدم باستخدام OAuth2.
# الدالة get_current_user تُحقن تلقائياً باستخدام Depends، فتتحقق من التوكن وتُرجع بيانات المستخدم، ثم يعرضها endpoint /profile.
"""

from fastapi import (
    Depends,
)  # استيراد Depends لاستخدام الاعتمادات في الـ FastAPI (لإدارة حقن الاعتمادية)

from app.auth.oauth2 import (
    get_current_user,
)  # استيراد دالة get_current_user للتحقق من المستخدم الحالي عبر OAuth2


@app.get("/profile")  # إنشاء endpoint GET على المسار /profile
async def profile(
    user=Depends(get_current_user),
):  # دالة async تستقبل المستخدم الحالي كاعتماد (Dependency Injection)
    return {"user": user}  # ترجع بيانات المستخدم الحالي على شكل JSON
