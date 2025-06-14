# 🧠 هذا الملف يحتوي على 3 Endpoints رئيسية:
# 1. POST /ai/prompts/ ➜ لإنشاء طلب جديد للذكاء الاصطناعي.
# 2. GET /ai/prompts/ ➜ لجلب كل الطلبات التي أنشأها المستخدم الحالي.
# 3. GET /ai/prompts/{id} ➜ لجلب طلب محدد مع الرد المرتبط به (إن وجد).
# يُستخدم هذا الملف لبناء واجهة REST لإدارة طلبات الذكاء الاصطناعي في النظام.

# 📁 المسار: app/routers/ai_prompts.py🧠 ملخص الملف:

# هذا الملف يحتوي على 3 Endpoints رئيسية:
# POST /ai/prompts/ → ينشئ Prompt وينفّذ توليد الرد من OpenAI ويخزن النتيجة.
# GET /ai/prompts/ → يعرض كل الطلبات الخاصة بالمستخدم الحالي.
# GET /ai/prompts/{prompt_id} → يعرض تفاصيل طلب معين والرد المرتبط به.
# يستخدم Depends(get_current_user) لضمان أن المستخدم مسجّل الدخول.
# يتكامل مع خدمة generate_ai_response لتوليد الردود.
# يعالج الحالات: success / failure / processing.

from fastapi import (
    APIRouter,
    Depends,
    HTTPException,
)  # أدوات إنشاء API ومسارات واعتماديات
from sqlalchemy.orm import Session  # جلسة قاعدة البيانات
from uuid import UUID  # للتعامل مع UUIDs في الـ id
from datetime import datetime  # لتسجيل وقت الإنشاء

from app.db.database import get_db  # دالة للحصول على جلسة قاعدة البيانات
from app.db.models.prompt_request import (
    PromptRequest,
    PromptStatus,
)  # نموذج الطلب وحالة الطلب
from app.db.models.prompt_response import PromptResponse  # نموذج الرد
from app.schemas.ai_prompts import (
    PromptCreate,
    PromptOut,
    PromptDetail,
)  # مخططات البيانات (schemas)
from app.dependencies.auth import (
    get_current_user,
)  # دالة المصادقة للحصول على المستخدم الحالي
from app.db.models.user import User  # نموذج المستخدم
from app.services.openai_generator import (
    generate_ai_response,
)  # دالة توليد الرد من OpenAI

router = APIRouter(
    prefix="/ai/prompts", tags=["AI Prompts"]
)  # إعداد الراوتر لمسارات الذكاء الاصطناعي


# 🔹 إرسال طلب جديد إلى الذكاء الاصطناعي وتنفيذ التوليد
# POST: AI Request (data from user) -> AI endpoint
@router.post("/", response_model=PromptOut)


# Create a new AI promt dpend on user input
def create_prompt(
    data: PromptCreate,  # البيانات القادمة من المستخدم لإنشاء الطلب
    db: Session = Depends(get_db),  # جلسة قاعدة البيانات من الاعتمادية
    current_user: User = Depends(get_current_user),  # المستخدم الحالي المستخرج من JWT
):
    # إنشاء كائن الطلب وتخزينه بالحالة "جاري المعالجة"
    prompt = PromptRequest(
        user_id=current_user.id,
        model=data.model,
        prompt_type=data.prompt_type,
        prompt_text=data.prompt_text,
        status=PromptStatus.processing,
        created_at=datetime.utcnow(),
    )
    db.add(prompt)
    db.commit()
    db.refresh(prompt)  # تحديث الكائن بعد الإدخال

    try:
        # توليد الرد من الذكاء الاصطناعي
        result = generate_ai_response(prompt.prompt_text, prompt.model)
        response = PromptResponse(
            prompt_id=prompt.id,
            response_text=result["response_text"],
            duration_ms=result["duration_ms"],
            created_at=datetime.utcnow(),
        )
        prompt.status = PromptStatus.completed  # تحديث الحالة إلى "تم"

        # Save Req in DB then send to ChatGPT to answer it
        db.add(response)
    except Exception as e:
        prompt.status = PromptStatus.failed  # لو حدث خطأ، نحدث الحالة إلى "فشل"
        db.add(prompt)
        db.commit()
        raise HTTPException(status_code=500, detail="AI generation failed")

    db.commit()

    # Finaly return ChatGPT ansur to the end user
    return prompt  # إرجاع الطلب بعد التنفيذ


# 🔹 جلب كل الطلبات الخاصة بالمستخدم الحالي
# GET: All the Current user Quetions from DB
@router.get("/", response_model=list[PromptOut])
def list_user_prompts(
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user),
):
    return (
        db.query(PromptRequest).filter(PromptRequest.user_id == current_user.id).all()
    )  # استعلام لكل الطلبات المرتبطة بالمستخدم الحالي

# 🔹 جلب طلب معين مع الرد إن وجد
# GET by ID from DB
@router.get("/{prompt_id}", response_model=PromptDetail)
def get_prompt(
    prompt_id: UUID,  # معرف الطلب المطلوب
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user),
):
    # جلب الطلب من قاعدة البيانات بشرط أنه يعود للمستخدم الحالي
    prompt = (
        db.query(PromptRequest)
        .filter(PromptRequest.id == prompt_id, PromptRequest.user_id == current_user.id)
        .first()
    )

    if not prompt:
        raise HTTPException(
            status_code=404, detail="Prompt not found"
        )  # لو الطلب غير موجود

    return prompt  # إرجاع تفاصيل الطلب مع الرد
