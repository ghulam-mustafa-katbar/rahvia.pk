from rest_framework import status, views, permissions
from rest_framework.response import Response
from django.http import HttpResponse
from django.shortcuts import get_object_or_404
from .models import Report, ReportRecommendation
from .serializers import ReportSerializer, ReportRecommendationSerializer
from .pdf_generator import generate_report_pdf
from students.models import Student

class ReportByStudentView(views.APIView):
    permission_classes = [permissions.IsAuthenticated]

    def get(self, request, student_id):
        student = get_object_or_404(Student, student_id=student_id)
        report = Report.objects.filter(student=student).order_by('-created_at').first()
        if not report:
            return Response({'error': 'No report found for this student. Complete an assessment first.'}, status=status.HTTP_404_NOT_FOUND)
        
        serializer = ReportSerializer(report)
        return Response(serializer.data)

class ReportDetailView(views.APIView):
    permission_classes = [permissions.IsAuthenticated]

    def get(self, request, report_id):
        report = get_object_or_404(Report, report_id=report_id)
        serializer = ReportSerializer(report)
        return Response(serializer.data)

class ReportPdfDownloadView(views.APIView):
    # Allow download without requiring Bearer auth header so direct link clicks,
    # browser navigation, and shared counselor/parent links work seamlessly.
    permission_classes = [permissions.AllowAny]
    authentication_classes = []

    def get(self, request, report_id):
        report = get_object_or_404(Report, report_id=report_id)
        pdf_bytes = generate_report_pdf(report)
        
        student_name = report.student.name if report.student else "Student"
        safe_name = "".join(c for c in student_name if c.isalnum() or c in (' ', '_', '-')).strip().replace(' ', '_')
        filename = f"Rahvia_Career_Report_{safe_name}_{report.created_at.strftime('%Y%m%d')}.pdf"
        
        disposition = 'inline' if request.GET.get('view') == 'inline' else 'attachment'
        
        response = HttpResponse(pdf_bytes, content_type='application/pdf')
        response['Content-Disposition'] = f'{disposition}; filename="{filename}"'
        response['Content-Length'] = len(pdf_bytes)
        response['Access-Control-Expose-Headers'] = 'Content-Disposition'
        return response

class RecommendationsByReportView(views.APIView):
    permission_classes = [permissions.IsAuthenticated]

    def get(self, request, report_id):
        report = Report.objects.filter(report_id=report_id).first()
        if report:
            recs = report.recommendations.all().order_by('rank')
            serializer = ReportRecommendationSerializer(recs, many=True)
            return Response(serializer.data)
        
        rec = get_object_or_404(ReportRecommendation, id=report_id)
        return Response(ReportRecommendationSerializer(rec).data)
