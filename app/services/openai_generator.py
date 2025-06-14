# 📦 app/services/openai_generator.py
# الملف هذا مسؤول عن:
# إرسال prompt_text لـ OpenAI.
# استلام response_text من الموديل.
# حساب الزمن المستغرق

# 📁 المسار: app/services/openai_generator.py

# 🧠 هذا الملف مسؤول عن:
# - الاتصال بمكتبة OpenAI لتوليد الردود الذكية.
# - إرسال prompt إلى API واسترجاع الرد مع حساب الزمن.
# - يُستخدم داخل الخدمات التي تحتاج إلى توليد محتوى آلي باستخدام الذكاء الاصطناعي.


import openai  # مكتبة OpenAI للتعامل مع نماذج الذكاء الاصطناعي مثل GPT
import time  # لحساب الزمن المستغرق في التوليد
import os  # للوصول إلى متغيرات البيئة
from dotenv import load_dotenv  # لتحميل متغيرات البيئة من ملف .env

load_dotenv()  # تحميل المتغيرات من ملف .env تلقائيًا

# 🔐 إعداد مفتاح OpenAI API من متغيرات البيئة
openai.api_key = os.getenv("OPENAI_API_KEY")  # تعيين المفتاح السري لاستخدام API


# ترسل نص الـ prompt إلى OpenAI وتعيد الرد الجاهز مع الوقت المستغرق بالمللي ثانية.
# Generate AI Response : this method do?
def generate_ai_response(
    prompt_text: str, model: str = "gpt-3.5-turbo"
):  # دالة لتوليد رد من الذكاء الاصطناعي باستخدام prompt معين
    start_time = time.time()  # بدء عداد الوقت لحساب المدة المستغرقة

    try:
        response = openai.ChatCompletion.create(  # استدعاء واجهة OpenAI لتوليد الرد من النموذج المختار
            model=model,  # تحديد النموذج (مثل gpt-3.5-turbo)
            messages=[
                {
                    "role": "user",
                    "content": prompt_text,
                }  # إرسال prompt بصيغة رسالة مستخدم
            ],
            temperature=0.7,  # درجة العشوائية في الرد
            max_tokens=1000,  # الحد الأقصى لعدد الكلمات في الرد
        )

        reply = response.choices[0].message.content  # استخراج النص الناتج من الرد
        duration = int((time.time() - start_time) * 1000)  # حساب المدة بالمللي ثانية

        return {
            "response_text": reply,  # نص الرد النهائي من الذكاء الاصطناعي
            "duration_ms": duration,  # المدة المستغرقة في توليد الرد
        }

    except Exception as e:
        raise RuntimeError(
            f"OpenAI generation failed: {str(e)}"
        )  # في حال حدوث خطأ، نرفع استثناء مخصص برسالة واضحة


"""


📦 generate_ai_response(prompt_text: str, model: str = "gpt-3.5-turbo")
✅ الوظيفة:



🧠 الشرح سطر بسطر:
python
Copy
Edit
start_time = time.time()
🔹 نبدأ عداد الوقت لحساب الزمن المستغرق في التوليد.

python
Copy
Edit
response = openai.ChatCompletion.create(
    model=model,
    messages=[
        {
            "role": "user",
            "content": prompt_text,
        }
    ],
    temperature=0.7,
    max_tokens=1000,
)
🔹 هذا هو الاستدعاء الرئيسي لمكتبة OpenAI:

model: اسم الموديل مثل "gpt-3.5-turbo" أو "gpt-4".

messages: قائمة المحادثة، ونرسل فقط رسالة واحدة من النوع "user".

temperature: درجة الإبداع والعشوائية (0 = ثابت، 1 = أكثر تنوع).

max_tokens: عدد الكلمات أو الرموز القصوى في الرد.

python
Copy
Edit
reply = response.choices[0].message.content
🔹 استخراج الرد النهائي من نتيجة OpenAI. الرد يكون في choices[0].message.content.

python
Copy
Edit
duration = int((time.time() - start_time) * 1000)
🔹 نحسب المدة الزمنية بالمللي ثانية منذ بداية التشغيل.

python
Copy
Edit
return {
    "response_text": reply,
    "duration_ms": duration,
}
🔹 نُعيد الرد كـ قاموس يحتوي على:

response_text: الرد من OpenAI.

duration_ms: الزمن المستغرق في توليد الرد.

python
Copy
Edit
except Exception as e:
    raise RuntimeError(f"OpenAI generation failed: {str(e)}")
🔺 إذا حصل أي خطأ (مثلاً API key ناقص أو timeout)، يتم رفع استثناء مخصص برسالة واضحة للمطور.

✅ مثال على الاستخدام:
python
Copy
Edit
result = generate_ai_response("اشرح لي الذكاء الاصطناعي", "gpt-4")
print(result)
🧾 الناتج المتوقع:

json
Copy
Edit
{
  "response_text": "الذكاء الاصطناعي هو...",
  "duration_ms": 812
}


📦 تلخيص سريع:
الخاصية	معناها
prompt_text	النص المطلوب إرساله لـ OpenAI
model	اسم النموذج (افتراضي gpt-3.5-turbo)
response_text	الرد الناتج من الذكاء الاصطناعي
duration_ms	الزمن المستغرق بالتوليد (ms)
التعامل مع الأخطاء	يتم رفع RuntimeError برسالة مفهومة


 """
