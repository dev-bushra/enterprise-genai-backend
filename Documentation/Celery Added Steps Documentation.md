رائع! 🔥

ننتقل الآن لتكامل **Celery** مع مشروعنا ليتم تشغيل مهام توليد الردود (Generate AI Response) في **الخلفية (Background Tasks)** بدل أن ننتظر الرد فورًا في طلب API.

---

## خطة العمل خطوة بخطوة لتكامل Celery:

### 1. تثبيت المتطلبات:

```bash
pip install celery[redis] redis
```

* `celery[redis]`: تثبيت Celery مع دعم Redis كوسيط للرسائل.
* `redis`: مكتبة بايثون للتعامل مع Redis.

---

### 2. تشغيل خادم Redis محليًا (أو استخدام Redis خدمة سحابية)

لو على جهازك، شغّل Redis server (مثلاً على لينكس):

```bash
redis-server
```

---

### 3. إعداد ملف `celery.py` في مجلد `app` ليكون نقطة انطلاق Celery في المشروع

```python
# app/celery.py

from celery import Celery
import os

CELERY_BROKER_URL = os.getenv("CELERY_BROKER_URL", "redis://localhost:6379/0")
CELERY_RESULT_BACKEND = os.getenv("CELERY_RESULT_BACKEND", "redis://localhost:6379/0")

celery_app = Celery(
    "app",
    broker=CELERY_BROKER_URL,
    backend=CELERY_RESULT_BACKEND,
    include=["app.tasks.ai_tasks"],
)

celery_app.conf.update(
    task_serializer="json",
    result_serializer="json",
    accept_content=["json"],
    timezone="UTC",
    enable_utc=True,
)
```

---

### 4. إنشاء ملف المهام `app/tasks/ai_tasks.py` لتعريف المهمة التي ستشغل التوليد في الخلفية

```python
# app/tasks/ai_tasks.py

from app.celery import celery_app
from app.services.openai_generator import generate_ai_response
from app.db.session import SessionLocal
from app.db.models.prompt_request import PromptRequest, PromptStatus
from app.db.models.prompt_response import PromptResponse
from sqlalchemy.orm import Session
import time

@celery_app.task(bind=True)
def generate_prompt_response_task(self, prompt_request_id: str):
    db: Session = SessionLocal()
    try:
        prompt_request = db.query(PromptRequest).filter(PromptRequest.id == prompt_request_id).first()
        if not prompt_request:
            return f"PromptRequest {prompt_request_id} not found"

        # تغيير الحالة إلى جاري التنفيذ
        prompt_request.status = PromptStatus.IN_PROGRESS
        db.commit()

        start_time = time.time()

        # استدعاء OpenAI لتوليد الرد
        response_text = generate_ai_response(prompt_request.model, prompt_request.prompt_text)

        duration_ms = int((time.time() - start_time) * 1000)

        # تخزين الرد في قاعدة البيانات
        prompt_response = PromptResponse(
            prompt_id=prompt_request.id,
            response_text=response_text,
            duration_ms=duration_ms,
        )
        db.add(prompt_response)

        # تحديث حالة الطلب إلى مكتمل
        prompt_request.status = PromptStatus.COMPLETED
        db.commit()

        return f"Task completed for PromptRequest {prompt_request_id}"

    except Exception as e:
        # في حال الخطأ، تحديث الحالة إلى فشل
        prompt_request.status = PromptStatus.FAILED
        db.commit()
        return str(e)
    finally:
        db.close()
```

---

### 5. تحديث الراوتر `ai_prompts.py` لتشغيل المهمة بالخلفية وليس التوليد فورًا

```python
# app/routers/ai_prompts.py

from fastapi import APIRouter, Depends, HTTPException
from app.schemas.ai_prompts import PromptCreate, PromptOut, PromptDetail
from app.db.session import get_db
from sqlalchemy.orm import Session
from app.db.models.prompt_request import PromptRequest, PromptStatus
from app.tasks.ai_tasks import generate_prompt_response_task
import uuid

router = APIRouter()

@router.post("/", response_model=PromptOut)
def create_prompt(prompt: PromptCreate, db: Session = Depends(get_db)):
    new_prompt = PromptRequest(
        id=str(uuid.uuid4()),
        user_id="some_user_id",  # عدّل حسب نظام المستخدمين لديك
        model=prompt.model,
        prompt_type=prompt.prompt_type,
        prompt_text=prompt.prompt_text,
        status=PromptStatus.PENDING,
    )
    db.add(new_prompt)
    db.commit()
    db.refresh(new_prompt)

    # تشغيل مهمة Celery في الخلفية
    generate_prompt_response_task.delay(new_prompt.id)

    return new_prompt
```

---

### 6. إعداد متغيرات البيئة (env)

```
CELERY_BROKER_URL=redis://localhost:6379/0
CELERY_RESULT_BACKEND=redis://localhost:6379/0
```

---

### 7. تشغيل خدمة Celery worker في التيرمنال

```bash
celery -A app.celery.celery_app worker --loglevel=info
```

---

### ملخص

* بدلاً من انتظار الرد من OpenAI API في نفس طلب الـ HTTP، نُنشئ المهمة في Celery لتُشغّل في الخلفية.
* المستخدم يستلم رد سريع بإنشاء الطلب مع حالة **Pending**.
* بعد انتهاء المهمة، يتم تحديث الرد في قاعدة البيانات وحالة الطلب إلى **Completed** أو **Failed**.
* يمكن للمستخدمين الاستعلام لاحقًا عن حالة الرد.

---

هل تريد أساعدك في:

* إضافة واجهة متابعة حالة الطلبات (polling أو WebSocket)؟
* شرح كيفية التعامل مع الأخطاء في Celery؟
* شرح كيفية تكامل Celery مع FastAPI بشكل أعمق؟
* أي شيء آخر؟

