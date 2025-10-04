# معمارية النظام - System Architecture

## نظرة عامة (Overview)

نظام ERP لمراكز الأوائل للرعاية النهارية مبني على معمارية الخدمات المصغرة (Microservices) لضمان المرونة، القابلية للتطوير، وسهولة الصيانة.

## الهيكل المعماري الشامل

```
┌─────────────────────────────────────────────────────────────────┐
│                    Client Applications                          │
│  ┌──────────┐  ┌──────────┐  ┌──────────┐  ┌──────────┐       │
│  │   Web    │  │  Mobile  │  │  Parent  │  │  Driver  │       │
│  │   App    │  │   App    │  │  Portal  │  │   App    │       │
│  └──────────┘  └──────────┘  └──────────┘  └──────────┘       │
└─────────────────────────────────────────────────────────────────┘
                              │
                              │ HTTPS/WSS
                              ▼
┌─────────────────────────────────────────────────────────────────┐
│                         Nginx (Reverse Proxy)                   │
│                    Load Balancer + SSL Termination              │
└─────────────────────────────────────────────────────────────────┘
                              │
                              ▼
┌─────────────────────────────────────────────────────────────────┐
│                        API Gateway                              │
│  - Authentication & Authorization (JWT)                         │
│  - Rate Limiting                                                │
│  - Request Routing                                              │
│  - API Versioning                                               │
└─────────────────────────────────────────────────────────────────┘
                              │
                              ▼
┌─────────────────────────────────────────────────────────────────┐
│                      Microservices Layer                        │
│                                                                 │
│  ┌──────────────┐  ┌──────────────┐  ┌──────────────┐         │
│  │   Student    │  │   Employee   │  │   Program    │         │
│  │   Service    │  │   Service    │  │   Service    │         │
│  └──────────────┘  └──────────────┘  └──────────────┘         │
│                                                                 │
│  ┌──────────────┐  ┌──────────────┐  ┌──────────────┐         │
│  │ Assessment   │  │  Financial   │  │     HR       │         │
│  │   Service    │  │   Service    │  │   Service    │         │
│  └──────────────┘  └──────────────┘  └──────────────┘         │
│                                                                 │
│  ┌──────────────┐  ┌──────────────┐  ┌──────────────┐         │
│  │     AI       │  │   Comm.      │  │  Reporting   │         │
│  │   Service    │  │   Service    │  │   Service    │         │
│  └──────────────┘  └──────────────┘  └──────────────┘         │
└─────────────────────────────────────────────────────────────────┘
                              │
                              ▼
┌─────────────────────────────────────────────────────────────────┐
│                   Message Broker (RabbitMQ)                     │
│              Asynchronous Communication Layer                    │
└─────────────────────────────────────────────────────────────────┘
                              │
                              ▼
┌─────────────────────────────────────────────────────────────────┐
│                        Data Layer                               │
│  ┌──────────────┐  ┌──────────────┐  ┌──────────────┐         │
│  │  PostgreSQL  │  │   MongoDB    │  │    Redis     │         │
│  │ (Relational) │  │ (Document)   │  │   (Cache)    │         │
│  └──────────────┘  └──────────────┘  └──────────────┘         │
└─────────────────────────────────────────────────────────────────┘
                              │
                              ▼
┌─────────────────────────────────────────────────────────────────┐
│                    Monitoring & Logging                         │
│  ┌──────────────┐  ┌──────────────┐  ┌──────────────┐         │
│  │  Prometheus  │  │   Grafana    │  │  ELK Stack   │         │
│  │ (Metrics)    │  │ (Dashboards) │  │   (Logs)     │         │
│  └──────────────┘  └──────────────┘  └──────────────┘         │
└─────────────────────────────────────────────────────────────────┘
```

## الخدمات المصغرة (Microservices)

### 1. Student Service (خدمة إدارة الطلاب)

**المسؤوليات:**
- تسجيل الطلاب وإدارة ملفاتهم
- إدارة البيانات الشخصية والطبية
- تتبع الحضور والغياب
- إدارة النقل والمواصلات

**تقنيات:**
- Python Flask
- PostgreSQL (البيانات المنظمة)
- MongoDB (الملفات والوثائق)

**Endpoints:**
```
POST   /api/students              # إضافة طالب
GET    /api/students              # قائمة الطلاب
GET    /api/students/{id}         # تفاصيل طالب
PUT    /api/students/{id}         # تحديث طالب
DELETE /api/students/{id}         # حذف طالب
GET    /api/students/{id}/profile # الملف الشخصي الشامل
```

### 2. Employee Service (خدمة إدارة الموظفين)

**المسؤوليات:**
- إدارة ملفات الموظفين
- نظام الصلاحيات (RBAC)
- تتبع الحضور والإجازات
- تقييم الأداء

**تقنيات:**
- Python Flask
- PostgreSQL

**Endpoints:**
```
POST   /api/employees             # إضافة موظف
GET    /api/employees             # قائمة الموظفين
GET    /api/employees/{id}        # تفاصيل موظف
POST   /api/employees/{id}/attendance  # تسجيل حضور
GET    /api/employees/{id}/performance # تقييم الأداء
```

### 3. Program Service (خدمة البرامج التأهيلية)

**المسؤوليات:**
- إدارة البرامج التأهيلية (7 أنواع)
- جدولة الجلسات
- تتبع التقدم
- إنشاء خطط IEP

**تقنيات:**
- Python Flask
- PostgreSQL
- MongoDB (للخطط والملاحظات)

**Endpoints:**
```
POST   /api/programs              # إنشاء برنامج
GET    /api/programs              # قائمة البرامج
POST   /api/programs/{id}/sessions  # جدولة جلسة
GET    /api/programs/{id}/progress  # تقدم البرنامج
POST   /api/programs/iep          # إنشاء خطة IEP
```

### 4. Assessment Service (خدمة التقييم)

**المسؤوليات:**
- إدارة التقييمات (383 مهارة)
- المقاييس الموحدة
- تقارير التقدم
- التحليلات

**تقنيات:**
- Python Flask
- PostgreSQL (النتائج)
- MongoDB (التقييمات التفصيلية)

**Endpoints:**
```
POST   /api/assessments           # إنشاء تقييم
GET    /api/assessments           # قائمة التقييمات
GET    /api/assessments/{id}      # تفاصيل تقييم
GET    /api/skills                # قائمة المهارات (383)
GET    /api/skills/categories     # فئات المهارات (13)
```

### 5. Financial Service (الخدمة المالية)

**المسؤوليات:**
- المحاسبة (شجرة الحسابات)
- قيود اليومية
- الفواتير والمدفوعات
- التقارير المالية

**تقنيات:**
- Python Flask
- PostgreSQL
- Redis (للتخزين المؤقت)

**Endpoints:**
```
POST   /api/finance/invoices      # إنشاء فاتورة
GET    /api/finance/accounts      # شجرة الحسابات
POST   /api/finance/journal       # قيد يومية
GET    /api/finance/reports       # التقارير المالية
```

### 6. AI Service (خدمة الذكاء الاصطناعي)

**المسؤوليات:**
- التحليلات التنبؤية
- التوصيات الذكية
- معالجة اللغة الطبيعية (NLP)
- Chatbot

**تقنيات:**
- Python FastAPI
- TensorFlow / PyTorch
- OpenAI API
- MongoDB (للبيانات غير المهيكلة)

**Endpoints:**
```
POST   /api/ai/predict            # تنبؤات
POST   /api/ai/recommend          # توصيات
POST   /api/ai/analyze            # تحليلات
POST   /api/ai/chatbot            # الدردشة
```

### 7. Communication Service (خدمة الاتصالات)

**المسؤوليات:**
- إرسال الرسائل النصية (SMS)
- البريد الإلكتروني
- WhatsApp Integration
- الإشعارات Push

**تقنيات:**
- Node.js (للاتصالات اللحظية)
- Redis (للطابور)
- Twilio API
- Firebase Cloud Messaging

**Endpoints:**
```
POST   /api/comm/sms              # إرسال SMS
POST   /api/comm/email            # إرسال Email
POST   /api/comm/whatsapp         # إرسال WhatsApp
POST   /api/comm/notification     # إرسال إشعار
```

### 8. Reporting Service (خدمة التقارير)

**المسؤوليات:**
- إنشاء التقارير
- لوحات المعلومات
- التصدير (PDF, Excel)
- الجدولة التلقائية

**تقنيات:**
- Python Flask
- PostgreSQL (للاستعلامات)
- Redis (للتخزين المؤقت)

**Endpoints:**
```
GET    /api/reports/students      # تقارير الطلاب
GET    /api/reports/financial     # التقارير المالية
GET    /api/reports/performance   # تقارير الأداء
POST   /api/reports/generate      # إنشاء تقرير
```

## قواعد البيانات

### PostgreSQL (البيانات المنظمة)

**الجداول الرئيسية:**
```sql
-- المستخدمون
users (id, name, email, password, role, created_at)

-- الطلاب
students (id, user_id, national_id, birth_date, gender, ...)

-- الموظفون
employees (id, user_id, specialization, hire_date, ...)

-- الفصول
classrooms (id, name, level, capacity, teacher_id, ...)

-- المهارات
skill_categories (id, name, description, order_index)
skills (id, category_id, skill_number, name, level, ...)

-- التقييمات
assessments (id, student_id, assessment_date, evaluator_name, ...)
skill_evaluations (id, assessment_id, skill_id, result, ...)

-- البرامج
programs (id, name, type, description, ...)
program_enrollments (id, student_id, program_id, ...)

-- المالية
accounts (id, name, code, type, parent_id, ...)
transactions (id, date, description, amount, ...)
invoices (id, student_id, amount, status, ...)
```

### MongoDB (البيانات غير المهيكلة)

**المجموعات:**
```javascript
// ملفات الطلاب الشاملة
student_files {
  _id: ObjectId,
  student_id: Number,
  documents: [
    {
      type: String,
      filename: String,
      path: String,
      uploaded_at: Date
    }
  ],
  medical_records: [],
  notes: []
}

// خطط IEP
iep_plans {
  _id: ObjectId,
  student_id: Number,
  plan_name: String,
  goals: [],
  strategies: [],
  progress: []
}

// سجلات الجلسات
therapy_sessions {
  _id: ObjectId,
  student_id: Number,
  therapist_id: Number,
  session_type: String,
  notes: String,
  activities: [],
  progress: {}
}

// تحليلات الذكاء الاصطناعي
ai_analytics {
  _id: ObjectId,
  student_id: Number,
  analysis_type: String,
  results: {},
  recommendations: [],
  created_at: Date
}
```

### Redis (التخزين المؤقت)

**الاستخدامات:**
```
# جلسات المستخدمين
session:{user_id} -> {session_data}

# التخزين المؤقت للبيانات
cache:students:list -> [students_data]
cache:student:{id} -> {student_data}

# الطوابير
queue:emails -> [email_jobs]
queue:sms -> [sms_jobs]

# معدلات الطلبات (Rate Limiting)
rate_limit:api:{ip}:{endpoint} -> counter
```

## الأمان (Security)

### المصادقة والترخيص

**JWT Token Structure:**
```json
{
  "header": {
    "alg": "HS256",
    "typ": "JWT"
  },
  "payload": {
    "user_id": 123,
    "email": "user@example.com",
    "role": "teacher",
    "exp": 1735689600
  }
}
```

**RBAC (Role-Based Access Control):**
```
Admin:
  - Full access to all resources
  
Manager:
  - Manage students, employees, programs
  - View financial reports
  
Teacher:
  - Manage assigned students
  - Create assessments
  - View assigned programs
  
Parent:
  - View own children only
  - Read-only access
```

### تشفير البيانات

**في حالة النقل (In Transit):**
- HTTPS/TLS 1.3
- WSS للاتصالات اللحظية

**في حالة السكون (At Rest):**
- AES-256 للبيانات الحساسة
- bcrypt لكلمات المرور

### الأمان على مستوى التطبيق

```python
# Rate Limiting
@limiter.limit("10 per minute")
def api_endpoint():
    pass

# Input Validation
from marshmallow import Schema, fields

class StudentSchema(Schema):
    name = fields.Str(required=True)
    national_id = fields.Str(required=True)
    # ...

# SQL Injection Prevention
# استخدام ORM (SQLAlchemy)
students = Student.query.filter_by(id=student_id).first()

# XSS Prevention
from markupsafe import escape
safe_output = escape(user_input)
```

## المراقبة والسجلات (Monitoring & Logging)

### Prometheus Metrics

```yaml
# Application Metrics
http_requests_total
http_request_duration_seconds
active_users
database_connections

# Business Metrics
students_enrolled_total
programs_completed_total
assessments_conducted_total
```

### Grafana Dashboards

**لوحات المعلومات:**
1. نظرة عامة على النظام
2. أداء التطبيق
3. قاعدة البيانات
4. مقاييس الأعمال
5. تنبيهات وأخطاء

### Logging Strategy

```python
import logging

# تكوين السجلات
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
    handlers=[
        logging.FileHandler('app.log'),
        logging.StreamHandler()
    ]
)

# السجلات حسب المستوى
logger.debug("Debug information")
logger.info("General information")
logger.warning("Warning message")
logger.error("Error occurred")
logger.critical("Critical issue")
```

## النشر (Deployment)

### Container Orchestration (Kubernetes)

```yaml
# deployment.yaml
apiVersion: apps/v1
kind: Deployment
metadata:
  name: alawael-app
spec:
  replicas: 3
  selector:
    matchLabels:
      app: alawael-app
  template:
    metadata:
      labels:
        app: alawael-app
    spec:
      containers:
      - name: app
        image: alawael/erp:latest
        ports:
        - containerPort: 5000
        env:
        - name: DATABASE_URI
          valueFrom:
            secretKeyRef:
              name: db-credentials
              key: uri
```

### CI/CD Pipeline

```yaml
# .gitlab-ci.yml
stages:
  - test
  - build
  - deploy

test:
  stage: test
  script:
    - pytest
    - flake8

build:
  stage: build
  script:
    - docker build -t alawael/erp:$CI_COMMIT_SHA .
    - docker push alawael/erp:$CI_COMMIT_SHA

deploy:
  stage: deploy
  script:
    - kubectl set image deployment/alawael-app app=alawael/erp:$CI_COMMIT_SHA
```

## القابلية للتطوير (Scalability)

### Horizontal Scaling

- استخدام Load Balancer (Nginx)
- تشغيل نسخ متعددة من كل خدمة
- Auto-scaling في Kubernetes

### Vertical Scaling

- زيادة موارد الخوادم حسب الحاجة
- تحسين الاستعلامات
- استخدام Indexing في قواعد البيانات

### Caching Strategy

```
1. Browser Cache (Static Files)
2. CDN (Images, Videos)
3. Redis Cache (API Responses)
4. Database Query Cache
```

## التعافي من الكوارث (Disaster Recovery)

### النسخ الاحتياطي

**جدول النسخ الاحتياطي:**
- يومياً في الساعة 2 صباحاً
- أسبوعياً (يوم السبت)
- شهرياً (أول كل شهر)

**الاحتفاظ:**
- النسخ اليومية: 7 أيام
- النسخ الأسبوعية: 4 أسابيع
- النسخ الشهرية: 12 شهراً

### خطة الاستعادة

```bash
# استعادة قاعدة البيانات
psql -U username -d dbname -f backup.sql

# استعادة الملفات
rsync -avz backup/uploads/ /app/uploads/
```

## الأداء (Performance)

### تحسينات الأداء

1. **Database Optimization:**
   - Indexing على الأعمدة المستخدمة كثيراً
   - Query Optimization
   - Connection Pooling

2. **Application Optimization:**
   - Lazy Loading
   - Pagination
   - Async Operations

3. **Caching:**
   - Redis للبيانات المتكررة
   - Browser Caching للموارد الثابتة

4. **CDN:**
   - توزيع المحتوى الثابت

### مؤشرات الأداء المستهدفة

- Response Time: < 200ms (95th percentile)
- Availability: 99.9% uptime
- Throughput: 1000 requests/second
- Database Query Time: < 50ms average

---

© 2024 مراكز الأوائل للرعاية النهارية - System Architecture
