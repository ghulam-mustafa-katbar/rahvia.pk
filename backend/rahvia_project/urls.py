from django.contrib import admin
from django.urls import path, include
from django.conf import settings
from django.conf.urls.static import static
from django.http import JsonResponse
from rest_framework_simplejwt.views import TokenRefreshView

def api_root(request):
    return JsonResponse({
        "status": "online",
        "service": "Rahvia Platform API",
        "frontend_url": "http://localhost:3000",
        "admin_panel": "/admin/",
        "sample_endpoints": [
            "/api/health",
            "/api/careers/",
            "/api/schools/",
            "/api/auth/login",
            "/api/assessment/start"
        ]
    })

def health_check(request):
    from django.db import connection
    from django.core.cache import cache
    
    db_ok = False
    cache_ok = False
    
    try:
        with connection.cursor() as cursor:
            cursor.execute("SELECT 1")
            row = cursor.fetchone()
            db_ok = bool(row and row[0] == 1)
    except Exception as e:
        db_ok = False
        
    try:
        cache.set('health_check_ping', 'pong', timeout=10)
        cache_ok = (cache.get('health_check_ping') == 'pong')
    except Exception as e:
        cache_ok = False
        
    status_code = 200 if (db_ok and cache_ok) else 503
    return JsonResponse({
        "status": "healthy" if status_code == 200 else "degraded",
        "database": "connected" if db_ok else "unreachable",
        "cache_redis": "connected" if cache_ok else "unreachable",
        "platform": "Pakistan National Career Encyclopedia & Student Assessment Platform",
        "environment": "production-ready"
    }, status=status_code)

from authentication.views import RegisterView, LoginView, CurrentUserView
from students.views import StudentProfileView
from assessments.views import (
    AssessmentStartView, AssessmentQuestionsView, AssessmentSubmitView,
    QuestionAdminListCreateView, QuestionAdminDetailView
)
from recommendations.views import (
    ReportByStudentView, ReportDetailView, ReportPdfDownloadView, RecommendationsByReportView
)
from careers.views import CareerFieldListCreateView, CareerFieldDetailView
from schools.views import SchoolListView, SchoolDashboardView, SchoolBatchEnrollView

admin.site.site_header = "Rahvia Education • Admin Portal"
admin.site.site_title = "Rahvia Admin"
admin.site.index_title = "EdTech Operations, Assessment Catalog & Cohort Analytics"

urlpatterns = [
    path('', api_root, name='api-root'),
    path('api/health', health_check, name='api-health'),
    path('admin/', admin.site.urls),

    # 1. Auth Endpoints
    path('api/auth/register', RegisterView.as_view(), name='api-register'),
    path('api/auth/login', LoginView.as_view(), name='api-login'),
    path('api/auth/me', CurrentUserView.as_view(), name='api-current-user'),
    path('api/auth/token/refresh', TokenRefreshView.as_view(), name='token-refresh'),

    # 2. Student Profile Endpoints
    path('api/student/profile', StudentProfileView.as_view(), name='api-student-profile'),

    # 3. Assessment Endpoints
    path('api/assessment/start', AssessmentStartView.as_view(), name='api-assessment-start'),
    path('api/assessment/<uuid:assessment_id>/questions', AssessmentQuestionsView.as_view(), name='api-assessment-questions'),
    path('api/assessment/<uuid:assessment_id>/submit', AssessmentSubmitView.as_view(), name='api-assessment-submit'),

    # 4. Reports & Recommendations Endpoints
    path('api/report/<uuid:student_id>', ReportByStudentView.as_view(), name='api-student-report'),
    path('api/report/detail/<uuid:report_id>', ReportDetailView.as_view(), name='api-report-detail'),
    path('api/report/<uuid:report_id>/pdf', ReportPdfDownloadView.as_view(), name='api-report-pdf'),
    path('api/recommendations/<uuid:report_id>', RecommendationsByReportView.as_view(), name='api-recommendations'),

    # 5. School Counselor & Cohort Analytics Endpoints
    path('api/schools/', SchoolListView.as_view(), name='api-schools-list'),
    path('api/school/<uuid:school_id>/dashboard', SchoolDashboardView.as_view(), name='api-school-dashboard'),
    path('api/school/<uuid:school_id>/batch-enroll', SchoolBatchEnrollView.as_view(), name='api-school-batch-enroll'),

    # 6. Career Fields Catalog / Encyclopedia
    path('api/careers/', CareerFieldListCreateView.as_view(), name='api-careers-list'),
    path('api/careers/<uuid:field_id>', CareerFieldDetailView.as_view(), name='api-careers-detail'),

    # 7. Admin Management Endpoints
    path('api/admin/questions', QuestionAdminListCreateView.as_view(), name='api-admin-questions'),
    path('api/admin/questions/<uuid:question_id>', QuestionAdminDetailView.as_view(), name='api-admin-question-detail'),
    path('api/admin/fields', CareerFieldListCreateView.as_view(), name='api-admin-fields'),
    path('api/admin/fields/<uuid:field_id>', CareerFieldDetailView.as_view(), name='api-admin-field-detail'),
]

if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
