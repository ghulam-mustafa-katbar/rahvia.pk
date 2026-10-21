from collections import Counter
from django.db.models import Avg
from django.shortcuts import get_object_or_404
from rest_framework import status, views, generics, permissions
from rest_framework.response import Response
from .models import School
from .serializers import SchoolSerializer, SchoolStudentRosterSerializer
from students.models import Student
from assessments.models import DimensionScore, AssessmentSession
from recommendations.models import Report
from authentication.models import User

class SchoolListView(generics.ListCreateAPIView):
    queryset = School.objects.all().order_by('name')
    serializer_class = SchoolSerializer
    permission_classes = [permissions.AllowAny]

class SchoolDashboardView(views.APIView):
    permission_classes = [permissions.IsAuthenticated]

    def get(self, request, school_id):
        school = get_object_or_404(School, school_id=school_id)
        students = Student.objects.filter(school=school).select_related('user')
        total_students = students.count()

        completed_assessments = AssessmentSession.objects.filter(
            student__school=school,
            status=AssessmentSession.StatusChoice.COMPLETED
        )
        assessed_student_ids = completed_assessments.values_list('student_id', flat=True).distinct()
        assessed_count = len(assessed_student_ids)

        # Calculate stream distribution from reports
        reports = Report.objects.filter(student__school=school).order_by('-created_at')
        stream_counter = Counter()
        for r in reports:
            if r.recommended_streams:
                stream_counter[r.recommended_streams[0]] += 1

        # Calculate average dimension percentiles for this cohort
        dim_avgs_qs = (
            DimensionScore.objects.filter(assessment__student__school=school)
            .values('dimension_name')
            .annotate(avg_pct=Avg('percentage'), avg_percentile=Avg('percentile'))
            .order_by('-avg_pct')
        )
        dimension_cohort_averages = {
            item['dimension_name']: {
                'avg_percentage': round(item['avg_pct'], 1) if item['avg_pct'] else 0.0,
                'avg_percentile': round(item['avg_percentile'], 1) if item['avg_percentile'] else 0.0
            }
            for item in dim_avgs_qs
        }

        # Students needing attention (e.g. low total score or no assessment yet)
        pending_students = students.exclude(student_id__in=assessed_student_ids).count()

        # Student roster serializer
        roster_data = SchoolStudentRosterSerializer(students[:100], many=True).data

        return Response({
            'school': SchoolSerializer(school).data,
            'summary': {
                'total_students': total_students,
                'assessed_students': assessed_count,
                'pending_assessment': pending_students,
                'completion_rate': round((assessed_count / total_students * 100), 1) if total_students > 0 else 0.0,
                'stream_distribution': dict(stream_counter),
                'dimension_averages': dimension_cohort_averages
            },
            'roster': roster_data
        })

class SchoolBatchEnrollView(views.APIView):
    permission_classes = [permissions.IsAuthenticated]

    def post(self, request, school_id):
        school = get_object_or_404(School, school_id=school_id)
        student_items = request.data.get('students', [])
        if not isinstance(student_items, list) or not student_items:
            return Response({'error': 'Expected a non-empty list of students.'}, status=status.HTTP_400_BAD_REQUEST)

        created_count = 0
        skipped_count = 0

        for item in student_items:
            email = str(item.get('email', '')).strip().lower()
            name = str(item.get('name', '')).strip()
            grade = str(item.get('grade', 'MATRIC_10TH'))
            if not email or not name:
                skipped_count += 1
                continue

            if User.objects.filter(email=email).exists():
                skipped_count += 1
                continue

            temp_password = item.get('password', 'StudentPass2026!')
            user = User.objects.create_user(
                email=email,
                password=temp_password,
                first_name=name.split()[0],
                last_name=" ".join(name.split()[1:]) if len(name.split()) > 1 else '',
                role=User.Role.STUDENT,
                parent_consent_granted=item.get('parent_consent', True)
            )

            Student.objects.create(
                user=user,
                school=school,
                name=name,
                board=school.board,
                current_grade=grade,
                elective_group=item.get('elective_group', 'SCIENCE_CS'),
                parent_consent=user.parent_consent_granted
            )
            created_count += 1

        return Response({
            'message': f'Batch enrollment completed. {created_count} registered, {skipped_count} skipped.',
            'created_count': created_count,
            'skipped_count': skipped_count
        }, status=status.HTTP_201_CREATED)
