🇸🇦 التوثيق العربي - دليل مطور Backend لمشروع AI Prompt Manager
🔥 مقدمة
نحن نعمل على بناء مشروع متكامل Enterprise Backend باستخدام FastAPI لإدارة نظام متقدم لإرسال واستقبال طلبات الذكاء الاصطناعي (AI Prompts) بطريقة منظمة، مرنة، وقابلة للتوسع.

المشروع يركز على:

تتبع كل طلبات الذكاء الاصطناعي والردود.

دعم عدة أنواع من النماذج (OpenAI، Gemini، غيرها).

نظام حالات متكامل (Pending, Completed, Failed).

التكامل مع خدمات خارجية (OpenAI API).

تخطيط لتشغيل المهام في الخلفية باستخدام Celery.

🎯 الهدف
توفير نظام backend متكامل لطلبات الذكاء الاصطناعي يمكن لأي خدمة أو فريق استخدامه بسهولة، مع إمكانية التوسع ودعم الموديلات الجديدة وإدارة الطلبات بفعالية.

⚙️ ما تم إنجازه حتى الآن
1. تصميم قاعدة البيانات (Database Design)
الجدول	الوصف
prompt_requests	جدول يحفظ طلبات المستخدمين (prompts)
prompt_responses	جدول يحفظ الردود الصادرة من نماذج AI

تفاصيل الجداول:
prompt_requests

الحقل	النوع	الوصف
id	UUID	معرف فريد للطلب
user_id	FK	معرف المستخدم الذي أرسل الطلب
model	String	اسم نموذج الذكاء الاصطناعي
prompt_type	String	نوع الطلب (نص، كود، تقرير...)
prompt_text	Text	نص الطلب
status	Enum	حالة الطلب (pending/completed/failed)
created_at	DateTime	تاريخ ووقت إنشاء الطلب

prompt_responses

الحقل	النوع	الوصف
id	UUID	معرف الرد
prompt_id	FK	معرف الطلب المرتبط بالرد
response_text	Text	نص الرد المولد من الذكاء الاصطناعي
created_at	DateTime	تاريخ ووقت حفظ الرد
duration_ms	Integer	مدة توليد الرد بالمللي ثانية

2. بناء SQLAlchemy Models
تم إنشاء موديلات PromptRequest و PromptResponse لتعكس الجداول السابقة.

كل موديل مرتبط بـ ORM Base ويتم إدارة الجداول تلقائيًا في PostgreSQL.

3. بناء API Endpoints باستخدام FastAPI
/ai/prompts/ (POST): لإنشاء طلب جديد.

/ai/prompts/ (GET): لجلب جميع الطلبات للمستخدم الحالي.

/ai/prompts/{id} (GET): لجلب تفاصيل طلب معين والرد الخاص به.

4. تعريف Schemas (Pydantic Models)
PromptCreate — بيانات إنشاء الطلب.

PromptOut — بيانات ملخصة لعرض الطلبات.

PromptDetail — بيانات تفصيلية مع الرد.

5. التكامل مع OpenAI API
عند استقبال طلب جديد، يتم:

حفظ الطلب في قاعدة البيانات.

إرسال النص إلى OpenAI API لتوليد الرد.

تخزين الرد والمدة المستغرقة في جدول الردود.

تحديث حالة الطلب (مكتمل أو فشل).

6. التخطيط للمستقبل: Celery + Redis
للاستفادة من المهام الخلفية (Background Tasks) وتشغيل توليد الردود بشكل غير متزامن.

تقليل زمن استجابة API.

دعم مهام طويلة ومعقدة.

📚 كيفية العمل لأي مطور جديد
إعداد البيئة الافتراضية وتثبيت المتطلبات (requirements.txt).

إعداد قاعدة البيانات PostgreSQL وربطها في app/db/database.py.

ضبط متغيرات البيئة .env، خصوصًا:

DATABASE_URL

OPENAI_API_KEY

تشغيل الميجريشن باستخدام Alembic لإنشاء الجداول.

تشغيل الخادم باستخدام uvicorn.

اختبار API عبر Swagger UI أو Postman.

🔗 المصادر الخارجية المستخدمة
PostgreSQL (قاعدة البيانات الرئيسية)

OpenAI API (توليد الردود)

FastAPI (إطار العمل الأساسي)

SQLAlchemy (ORM)

Pydantic (التحقق من صحة البيانات)

Alembic (إدارة الميجريشن)

Celery و Redis (مخطط للاستخدام مستقبليًا)

