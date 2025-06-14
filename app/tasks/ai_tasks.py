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
        prompt_request = (
            db.query(PromptRequest)
            .filter(PromptRequest.id == prompt_request_id)
            .first()
        )
        if not prompt_request:
            return f"PromptRequest {prompt_request_id} not found"

        # تغيير الحالة إلى جاري التنفيذ
        prompt_request.status = PromptStatus.IN_PROGRESS
        db.commit()

        start_time = time.time()

        # استدعاء OpenAI لتوليد الرد
        response_text = generate_ai_response(
            prompt_request.model, prompt_request.prompt_text
        )

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
