# Rahvia: Pakistan Student Career-Guidance Platform (MVP to Scale)

> **Role**: Principal Full-Stack Architect & EdTech Engineering Lead  
> **Context**: High-accessibility, data-driven career guidance portal tailored for Pakistani students (Matric / Intermediate boards: FBISE, BISE), schools, and administrators, adhering to local privacy and compliance standards (Pakistani PDPA draft rules).

---

## 1. Architectural Blueprint & Tech Stack

```
[ React 19 PWA + Tailwind CSS (Bilingual EN/UR) ]
                         │
                   (REST / JSON + JWT)
                         │
                         ▼
┌────────────────────────────────────────────────────────┐
│                   Django 6.1 + DRF                     │
│  ┌──────────────────┐  ┌────────────────────────────┐  │
│  │  Authentication  │  │   Assessment Scoring Engine│  │
│  │   (Bcrypt, PDPA) │  │   (Cognitive & RIASEC)     │  │
│  └──────────────────┘  └────────────────────────────┘  │
│  ┌──────────────────┐  ┌────────────────────────────┐  │
│  │ School Analytics │  │ Stream Recommendation Map  │  │
│  │ (Cohort Trends)  │  │  (FSc / ICS / I.Com / FA)  │  │
│  └──────────────────┘  └────────────────────────────┘  │
│  ┌──────────────────┐  ┌────────────────────────────┐  │
│  │  Career Catalog  │  │ ReportLab PDF Generator    │  │
│  │  (~500 Taxonomy) │  │ (Instant Downloadable Doc) │  │
│  └──────────────────┘  └────────────────────────────┘  │
└────────────────────────────────────────────────────────┘
          │                                  │
          ▼                                  ▼
[ PostgreSQL 16 (ACID/Relational) ]   [ Redis 7 (Cache/Queue) ]
```

- **Backend**: Python 3.13 / Django 6.1, Django REST Framework, SimpleJWT authentication, Bcrypt password hashing, and built-in Admin console.
- **Frontend**: React 19, Vite, Tailwind CSS with mobile-first layout, full Urdu typography support, and PWA capabilities for low-bandwidth rural accessibility.
- **Engines**: 
  - Dynamic Psychometric Assessment Engine (Cognitive aptitude + Holland RIASEC interest model).
  - Rule-Based Stream & Degree Recommendation Engine tailored for Pakistani admission standards (Pre-Engineering, Pre-Medical, ICS, Commerce, Humanities).
  - ReportLab PDF generator rendering verifiable student pathway dossiers.
- **Database & Cache**: PostgreSQL (with SQLite zero-config local fallback) + Redis caching.
- **Containerization**: Production multi-stage `Dockerfile` (Backend + Frontend Nginx) and `docker-compose.yml`.

---

## 2. Implemented Modules

### 1. Student Portal & Auth
- **JWT-based Authentication** with Role-Based Access Control (`STUDENT`, `COUNSELOR`, `ADMIN`).
- **Academic Profile Management**: Tracks educational board (`FBISE Islamabad`, `BISE Lahore`, `BISE Karachi`, etc.), grade level (`Matric 9th/10th`, `Inter 11th/12th`, `O/A Levels`), elective streams, and subject marks.
- **Pakistani PDPA Compliance**: Verifiable guardian/parental consent tracking for minors, recording consent timestamp and IP address.

### 2. Dynamic Psychometric Assessment Engine
- Multi-section modular question bank tagged by category (`APTITUDE`, `INTEREST`, `ACADEMIC`) and dimension (`NumericalAptitude`, `VerbalReasoning`, `SpatialVisualization`, `RIASEC_Realistic`, `RIASEC_Investigative`, `RIASEC_Social`, etc.).
- Complete bilingual question rendering (English and Urdu).
- Automated raw score aggregation and norm-referenced percentile computation.

### 3. Recommendation & Reporting Engine
- Hybrid mapping logic correlating cognitive metrics, Holland RIASEC interest factors, and school marks with Pakistani educational streams:
  - **FSc Pre-Engineering**: High Math, Spatial visualization, Realistic interest, ECAT/NET preparation.
  - **FSc Pre-Medical**: High Biology, Chemistry, Investigative interest, MDCAT preparation.
  - **ICS (Computer Science)**: High Math, Logical reasoning, Computing affinity, FAST/NET preparation.
  - **I.Com / Commerce**: Math, Verbal, Conventional, and Enterprising factors, CA/ACCA pathways.
  - **FA / Humanities & Law**: Verbal reasoning, Social interest, LAT (Law Admission Test) preparation.
- Generates strengths/growth areas breakdown, matching career fields, and downloadable PDF reports.

### 4. School Counselor Dashboard
- Aggregated cohort statistics: Total enrolled, assessment completion rate, and pending test tracking.
- Cohort Stream Distribution analysis and dimension score averages.
- Student roster data table with search, completion badges, and one-click report view.
- Batch student enrollment interface (CSV / multi-line import).

### 5. Super Admin Console
- Question bank management: Create and edit standardized items with Urdu translations, dimension keys, and options.
- Career fields catalog manager: Add degree pathways, entrance exams, and university affiliations.

---

## 3. Database Schema Blueprint

| Table | Primary Key | Key Fields & Foreign Keys |
| :--- | :--- | :--- |
| `User` | `id` (UUID) | `email`, `role`, `parent_consent_granted`, `parent_consent_date`, `parent_consent_ip` |
| `School` | `school_id` (UUID) | `name`, `code` (Unique), `board`, `city`, `province`, `contact_email` |
| `Student` | `student_id` (UUID) | `user_id` (FK), `school_id` (FK), `name`, `board`, `current_grade`, `elective_group`, `academic_scores` (JSON) |
| `Question` | `question_id` (UUID) | `text`, `text_urdu`, `type`, `category`, `dimension`, `options` (JSON), `correct_answer`, `correct_answer_weight` |
| `AssessmentSession` | `assessment_id` (UUID) | `student_id` (FK), `assessment_type`, `status`, `total_score`, `time_spent_seconds`, `date_taken` |
| `Response` | `response_id` (UUID) | `assessment_id` (FK), `question_id` (FK), `student_answer`, `score_awarded` |
| `DimensionScore` | `score_id` (UUID) | `assessment_id` (FK), `dimension_name`, `raw_score`, `max_possible`, `percentage`, `percentile` |
| `CareerField` | `field_id` (UUID) | `name`, `category`, `stream_requirement`, `typical_degrees` (JSON), `required_exams` (JSON), `top_universities_pakistan` (JSON) |
| `Report` | `report_id` (UUID) | `assessment_id` (FK/Unique), `student_id` (FK), `summary_narrative`, `recommended_streams` (JSON), `strengths` (JSON), `growth_areas` (JSON), `next_steps` (JSON) |
| `ReportRecommendation` | `id` (UUID) | `report_id` (FK), `field_id` (FK), `match_score`, `rationale_text`, `rank` |

---

## 4. RESTful API Specification

| Endpoint | Method | Description |
| :--- | :--- | :--- |
| `/api/auth/register` | `POST` | Registers student or counselor account; captures PDPA parental consent |
| `/api/auth/login` | `POST` | Authenticates credentials and issues JWT access & refresh tokens |
| `/api/auth/me` | `GET` | Returns current authenticated user and linked student profile |
| `/api/student/profile` | `GET/PUT` | Retrieves and updates student academic grades, board, and elective stream |
| `/api/assessment/start` | `POST` | Initializes dynamic assessment session |
| `/api/assessment/{id}/questions` | `GET` | Assembles modular question bank tailored to student's grade level |
| `/api/assessment/{id}/submit` | `POST` | Calculates raw/percentile dimension scores, executes recommendation engine, and returns `report_id` |
| `/api/report/{student_id}` | `GET` | Fetches the latest career pathway report for a student |
| `/api/report/detail/{report_id}` | `GET` | Fetches full report details including matched careers and scores |
| `/api/report/{report_id}/pdf` | `GET` | Downloads professional ReportLab PDF pathway report |
| `/api/recommendations/{report_id}` | `GET` | Retrieves ranked career recommendations with rationale texts |
| `/api/schools/` | `GET` | Lists partner institutions and colleges |
| `/api/school/{id}/dashboard` | `GET` | Returns cohort aggregated statistics, stream distribution, and student roster |
| `/api/school/{id}/batch-enroll` | `POST` | Batch registers student rosters under an institution |
| `/api/careers/` | `GET` | Searchable directory of Pakistani degree pathways and career fields |
| `/api/admin/questions` | `GET/POST` | Super Admin psychometric question bank management |
| `/api/admin/fields` | `GET/POST` | Super Admin career catalog and university mapping management |

---

## 5. Seed Test Credentials

Run `python manage.py seed_data` to populate:

- **Student Demo**: `student@rahvia.pk` / `Password123!` (Aisha Khan, Matric 10th Science CS, FBISE Islamabad)
- **School Counselor Demo**: `counselor@rahvia.pk` / `Password123!` (Dr. Tariq Mehmood, Islamabad Model College)
- **Super Administrator Demo**: `admin@rahvia.pk` / `Password123!`

---

## 6. How to Run Locally

### Backend Setup:
```powershell
# Navigate to backend directory
cd backend

# Activate virtual environment
..\venv\Scripts\Activate.ps1

# Run migrations
python manage.py migrate

# Seed question bank and careers catalog
python manage.py seed_data

# Run backend test suite
python manage.py test assessments

# Start Django development server
python manage.py runserver 0.0.0.0:8000
```

### Frontend Setup:
```powershell
# Navigate to frontend directory
cd frontend

# Install packages
npm install

# Build production bundle
npm run build

# Start Vite development server (proxies to backend on port 8000)
npm run dev
```

### Run with Docker Compose:
```bash
docker compose up --build
```
The frontend will be accessible at `http://localhost:3000` (or port 80), and the backend API at `http://localhost:8000`.
