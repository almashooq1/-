# API Documentation - نظام ERP

## المصادقة (Authentication)

### تسجيل الدخول
**Endpoint:** `POST /api/login`

**Request Body:**
```json
{
  "username": "user@example.com",
  "password": "password123"
}
```

**Response:**
```json
{
  "success": true,
  "access_token": "eyJ0eXAiOiJKV1QiLCJhbGc...",
  "user": {
    "id": 1,
    "name": "اسم المستخدم",
    "email": "user@example.com",
    "role": "admin"
  }
}
```

## الطلاب (Students)

### قائمة الطلاب
**Endpoint:** `GET /api/students`

**Query Parameters:**
- `search` (optional): البحث في الاسم أو رقم الهوية
- `classroom_id` (optional): تصفية حسب الفصل

**Response:**
```json
{
  "success": true,
  "students": [
    {
      "id": 1,
      "national_id": "1234567890",
      "name": "محمد أحمد",
      "birth_date": "2015-05-10",
      "gender": "male",
      "classroom_name": "الفصل الأول"
    }
  ]
}
```

### إضافة طالب
**Endpoint:** `POST /api/students`

**Request Body:**
```json
{
  "national_id": "1234567890",
  "name": "محمد أحمد",
  "birth_date": "2015-05-10",
  "gender": "male",
  "guardian_name": "أحمد محمد",
  "guardian_phone": "0501234567",
  "guardian_email": "parent@example.com",
  "classroom_id": 1
}
```

## التقييمات (Assessments)

### إنشاء تقييم
**Endpoint:** `POST /api/assessments`

**Request Body:**
```json
{
  "student_id": 1,
  "notes": "ملاحظات التقييم",
  "skill_evaluations": [
    {
      "skill_id": 1,
      "evaluation_result": "مكتسب"
    }
  ]
}
```

## خدمات الذكاء الاصطناعي

### تحليل تقدم الطالب
**Endpoint:** `POST /api/ai/student/analyze-progress`

**Request Body:**
```json
{
  "student_id": 1,
  "time_period": "last_month"
}
```

**Response:**
```json
{
  "success": true,
  "analysis": {
    "progress_score": 85,
    "strengths": ["المهارات الحركية", "التواصل"],
    "areas_for_improvement": ["المهارات الأكاديمية"],
    "recommendations": ["زيادة التركيز على القراءة"]
  }
}
```

## رموز الحالة (Status Codes)
- 200: نجاح
- 201: تم الإنشاء بنجاح
- 400: خطأ في الطلب
- 401: غير مصرح
- 404: غير موجود
- 500: خطأ في الخادم
