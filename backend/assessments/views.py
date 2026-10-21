from rest_framework import status, views, generics, permissions
from rest_framework.response import Response
from django.shortcuts import get_object_or_404
from .models import AssessmentSession, Question, Response as StudentResponse
from .serializers import (
    AssessmentSessionSerializer, QuestionSerializer, QuestionAdminSerializer,
    AssessmentStartSerializer, AssessmentSubmitSerializer
)
from .engine import process_assessment_submission
from recommendations.engine import evaluate_and_generate_report
from students.models import Student
from careers.views import IsAdminOrReadOnly

class AssessmentStartView(views.APIView):
    permission_classes = [permissions.IsAuthenticated]

    def post(self, request):
        serializer = AssessmentStartSerializer(data=request.data)
        if not serializer.is_valid():
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

        user = request.user
        student_id = serializer.validated_data.get('student_id')
        
        if student_id:
            # Counselor or admin starting on behalf of student
            student = get_object_or_404(Student, student_id=student_id)
        else:
            if hasattr(user, 'student_profile') and user.student_profile:
                student = user.student_profile
            else:
                # Auto-provision or retrieve profile so user is never blocked
                from schools.models import School
                default_school = School.objects.first()
                student, _ = Student.objects.get_or_create(
                    user=user,
                    defaults={
                        'name': user.get_full_name() or user.email.split('@')[0],
                        'school': default_school,
                        'current_grade': Student.GradeChoice.MATRIC_10,
                        'elective_group': Student.ElectiveChoice.SCIENCE_COMPUTER,
                        'board': 'BIEK Karachi'
                    }
                )

        assessment_type = serializer.validated_data.get('assessment_type', AssessmentSession.AssessmentType.COMPREHENSIVE)

        session = AssessmentSession.objects.create(
            student=student,
            assessment_type=assessment_type,
            status=AssessmentSession.StatusChoice.IN_PROGRESS
        )

        return Response({
            'message': 'Assessment session initialized.',
            'assessment_id': str(session.assessment_id),
            'assessment_type': session.assessment_type,
            'student_id': str(student.student_id),
            'student_name': student.name
        }, status=status.HTTP_201_CREATED)

class AssessmentQuestionsView(views.APIView):
    permission_classes = [permissions.IsAuthenticated]

    def get(self, request, assessment_id):
        session = get_object_or_404(AssessmentSession, assessment_id=assessment_id)
        student = session.student

        # Dynamic question assembly based on grade & assessment type
        qs = Question.objects.filter(is_active=True)
        grade = student.current_grade

        if 'MATRIC' in grade:
            qs = qs.filter(target_audience__in=[Question.TargetAudienceChoice.ALL, Question.TargetAudienceChoice.MATRIC])
        elif 'INTER' in grade or 'A_LEVELS' in grade:
            qs = qs.filter(target_audience__in=[Question.TargetAudienceChoice.ALL, Question.TargetAudienceChoice.INTER])

        questions = qs.order_by('category', 'order', 'created_at')
        serializer = QuestionSerializer(questions, many=True)
        return Response({
            'assessment_id': str(session.assessment_id),
            'total_questions': questions.count(),
            'questions': serializer.data
        })

class AssessmentSubmitView(views.APIView):
    permission_classes = [permissions.IsAuthenticated]

    def post(self, request, assessment_id):
        session = get_object_or_404(AssessmentSession, assessment_id=assessment_id)
        serializer = AssessmentSubmitSerializer(data=request.data)
        if not serializer.is_valid():
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

        answers = serializer.validated_data['answers']
        time_spent = serializer.validated_data.get('time_spent_seconds', 0)
        session.time_spent_seconds = time_spent

        # Execute scoring pipeline
        score_result = process_assessment_submission(session, answers)

        # Trigger recommendation and reporting engine
        report = evaluate_and_generate_report(session)

        return Response({
            'message': 'Assessment submitted and scored successfully.',
            'assessment_id': str(session.assessment_id),
            'student_id': str(session.student.student_id),
            'total_score': score_result['total_score'],
            'dimensions': score_result['dimensions'],
            'report_id': str(report.report_id)
        }, status=status.HTTP_200_OK)

class IsAdminUserOnly(permissions.BasePermission):
    """Ensures question answer keys and admin actions are strictly limited to authenticated staff and administrators."""
    def has_permission(self, request, view):
        return bool(request.user and request.user.is_authenticated and (request.user.is_staff or getattr(request.user, 'role', '') == 'ADMIN'))

class QuestionAdminListCreateView(generics.ListCreateAPIView):
    queryset = Question.objects.all().order_by('category', 'order')
    serializer_class = QuestionAdminSerializer
    permission_classes = [IsAdminUserOnly]

class QuestionAdminDetailView(generics.RetrieveUpdateDestroyAPIView):
    queryset = Question.objects.all()
    serializer_class = QuestionAdminSerializer
    permission_classes = [IsAdminUserOnly]
    lookup_field = 'question_id'
