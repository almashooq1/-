# دليل API

## نظرة عامة
هذا الدليل يوثق نقاط النهاية (Endpoints) المتاحة في API نظام مراكز الأوائل للرعاية النهارية.

## المصادقة
جميع نقاط النهاية (باستثناء تسجيل الدخول والتسجيل) تتطلب JWT Token في رأس الطلب:

```
Authorization: Bearer <token>
```

## نقاط النهاية الأساسية

### المصادقة

#### تسجيل الدخول
```http
POST /api/login
Content-Type: application/json

{
  "username": "email@example.com أو رقم الهوية",
  "password": "كلمة المرور"
}
```

**الاستجابة الناجحة:**
```json
{
  "success": true,
  "message": "تم تسجيل الدخول بنجاح",
  "access_token": "eyJ0eXAiOiJKV1QiLCJhbGc...",
  "user": {
    "id": 1,
    "name": "اسم المستخدم",
    "email": "email@example.com",
    "role": "admin"
  }
}
```

#### التسجيل
```http
POST /api/register
Content-Type: application/json

{
  "name": "الاسم الكامل",
  "email": "email@example.com",
  "national_id": "1234567890",
  "password": "كلمة المرور",
  "phone": "0501234567",
  "role": "teacher"
}
```

#### الحصول على بيانات المستخدم الحالي
```http
GET /api/me
Authorization: Bearer <token>
```

---

### الطلاب

#### قائمة الطلاب
```http
GET /api/students
Authorization: Bearer <token>
```

**المعاملات الاختيارية:**
- `search`: البحث في الأسماء والهويات
- `classroom_id`: تصفية حسب الفصل

#### إضافة طالب جديد
```http
POST /api/students
Authorization: Bearer <token>
Content-Type: application/json

{
  "national_id": "1234567890",
  "name": "اسم الطالب",
  "birth_date": "2015-01-01",
  "gender": "ذكر",
  "guardian_name": "اسم ولي الأمر",
  "guardian_phone": "0501234567",
  "guardian_email": "parent@example.com",
  "address": "العنوان",
  "medical_notes": "ملاحظات طبية",
  "classroom_id": 1
}
```

#### تفاصيل طالب
```http
GET /api/students/{student_id}
Authorization: Bearer <token>
```

#### تحديث بيانات طالب
```http
PUT /api/students/{student_id}
Authorization: Bearer <token>
Content-Type: application/json

{
  "name": "الاسم المحدث",
  "guardian_phone": "0509876543",
  ...
}
```

#### حذف طالب
```http
DELETE /api/students/{student_id}
Authorization: Bearer <token>
```

#### نقل طالب
```http
POST /api/students/{student_id}/transfer
Authorization: Bearer <token>
Content-Type: application/json

{
  "classroom_id": 2,
  "reason": "سبب النقل"
}
```

---

### المعلمين

#### قائمة المعلمين
```http
GET /api/teachers
Authorization: Bearer <token>
```

#### إضافة معلم جديد
```http
POST /api/teachers
Authorization: Bearer <token>
Content-Type: application/json

{
  "national_id": "1234567890",
  "name": "اسم المعلم",
  "email": "teacher@example.com",
  "phone": "0501234567",
  "specialization": "التخصص",
  "qualification": "المؤهل",
  "experience_years": 5,
  "hire_date": "2020-01-01",
  "salary": 5000
}
```

---

### الفصول الدراسية

#### قائمة الفصول
```http
GET /api/classrooms
Authorization: Bearer <token>
```

#### إنشاء فصل جديد
```http
POST /api/classrooms
Authorization: Bearer <token>
Content-Type: application/json

{
  "name": "الفصل الأول",
  "level": "المستوى الأول",
  "capacity": 20,
  "teacher_id": 1
}
```

---

### تقييم المهارات

#### قائمة المهارات
```http
GET /api/skills
Authorization: Bearer <token>
```

**المعاملات:**
- `domain_id`: تصفية حسب المجال
- `search`: البحث في المهارات

#### إنشاء تقييم
```http
POST /api/assessments
Authorization: Bearer <token>
Content-Type: application/json

{
  "student_id": 1,
  "notes": "ملاحظات التقييم",
  "skill_evaluations": [
    {
      "skill_id": 1,
      "evaluation_result": "متقن"
    },
    {
      "skill_id": 2,
      "evaluation_result": "غير متقن"
    }
  ]
}
```

---

### العيادات المتخصصة

#### قائمة العيادات
```http
GET /api/clinic-types
Authorization: Bearer <token>
```

#### حجز موعد
```http
POST /api/clinic-appointments
Authorization: Bearer <token>
Content-Type: application/json

{
  "clinic_type_id": 1,
  "specialist_id": 1,
  "student_id": 1,
  "appointment_date": "2024-01-15",
  "appointment_time": "10:00",
  "duration": 30,
  "reason": "سبب الموعد"
}
```

#### قائمة المواعيد
```http
GET /api/clinic-appointments
Authorization: Bearer <token>
```

**المعاملات:**
- `clinic_id`: تصفية حسب العيادة
- `specialist_id`: تصفية حسب الأخصائي
- `student_id`: تصفية حسب الطالب
- `status`: تصفية حسب الحالة

---

### إدارة الطوارئ

#### قائمة الحوادث
```http
GET /api/emergency/incidents
Authorization: Bearer <token>
```

#### تسجيل حادث جديد
```http
POST /api/emergency/incidents
Authorization: Bearer <token>
Content-Type: application/json

{
  "incident_type": "حريق",
  "emergency_level": "critical",
  "description": "وصف الحادث",
  "location": "الموقع",
  "incident_time": "2024-01-15T10:30:00",
  "affected_persons": 5
}
```

---

## رموز الحالة

- `200 OK` - نجاح الطلب
- `201 Created` - تم إنشاء المورد بنجاح
- `400 Bad Request` - خطأ في البيانات المرسلة
- `401 Unauthorized` - غير مصرح (token غير صالح أو مفقود)
- `404 Not Found` - المورد غير موجود
- `500 Internal Server Error` - خطأ في الخادم

## معالجة الأخطاء

جميع الأخطاء تُرجع بالتنسيق التالي:
```json
{
  "success": false,
  "error": "رسالة الخطأ"
}
```

## الترقيم (Pagination)

بعض النقاط تدعم الترقيم:
```http
GET /api/students?page=1&perPage=10
```

الاستجابة تحتوي على:
```json
{
  "success": true,
  "items": [...],
  "pagination": {
    "page": 1,
    "pages": 5,
    "per_page": 10,
    "total": 50
  }
}
```

## ملاحظات
- جميع التواريخ بتنسيق ISO 8601: `YYYY-MM-DD`
- جميع الأوقات بتنسيق 24 ساعة: `HH:MM`
- الاستجابات بصيغة JSON
- يُفضل استخدام HTTPS في الإنتاج
