from rest_framework import serializers
from .models import Report, ReportRecommendation
from careers.serializers import CareerFieldSerializer
from assessments.serializers import DimensionScoreSerializer

class ReportRecommendationSerializer(serializers.ModelSerializer):
    field_details = CareerFieldSerializer(source='field', read_only=True)

    class Meta:
        model = ReportRecommendation
        fields = [
            'id', 'field', 'field_details', 'match_score',
            'rationale_text', 'rationale_text_urdu', 'rank'
        ]

class ReportSerializer(serializers.ModelSerializer):
    recommendations = ReportRecommendationSerializer(many=True, read_only=True)
    dimension_scores = DimensionScoreSerializer(source='assessment.dimension_scores', many=True, read_only=True)
    student_name = serializers.CharField(source='student.name', read_only=True)
    school_name = serializers.CharField(source='student.school.name', default='', read_only=True)
    board = serializers.CharField(source='student.board', read_only=True)
    grade = serializers.CharField(source='student.get_current_grade_display', read_only=True)

    class Meta:
        model = Report
        fields = [
            'report_id', 'assessment', 'student', 'student_name', 'school_name',
            'board', 'grade', 'summary_narrative', 'summary_narrative_urdu',
            'strengths', 'growth_areas', 'recommended_streams', 'pathway_details',
            'cognitive_scores_snapshot', 'riasec_scores_snapshot', 'academic_interests_snapshot',
            'next_steps', 'recommendations', 'dimension_scores', 'created_at'
        ]
