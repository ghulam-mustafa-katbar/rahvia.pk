from rest_framework import serializers
from .models import AssessmentSession, Question, Response, DimensionScore
from students.models import Student

class QuestionSerializer(serializers.ModelSerializer):
    class Meta:
        model = Question
        fields = [
            'question_id', 'text', 'text_urdu', 'type', 'category',
            'dimension', 'subcategory', 'difficulty', 'target_audience', 'options', 'order'
        ]

class QuestionAdminSerializer(serializers.ModelSerializer):
    class Meta:
        model = Question
        fields = '__all__'

class DimensionScoreSerializer(serializers.ModelSerializer):
    class Meta:
        model = DimensionScore
        fields = ['score_id', 'dimension_name', 'raw_score', 'max_possible', 'percentage', 'percentile']

class ResponseSerializer(serializers.ModelSerializer):
    class Meta:
        model = Response
        fields = ['response_id', 'question', 'student_answer', 'score_awarded', 'time_taken_seconds']

class AssessmentSessionSerializer(serializers.ModelSerializer):
    dimension_scores = DimensionScoreSerializer(many=True, read_only=True)
    student_name = serializers.CharField(source='student.name', read_only=True)

    class Meta:
        model = AssessmentSession
        fields = [
            'assessment_id', 'student', 'student_name', 'assessment_type',
            'status', 'date_taken', 'completed_at', 'total_score',
            'time_spent_seconds', 'dimension_scores'
        ]
        read_only_fields = ['assessment_id', 'date_taken', 'completed_at', 'total_score']

class AssessmentStartSerializer(serializers.Serializer):
    student_id = serializers.UUIDField(required=False)
    assessment_type = serializers.ChoiceField(
        choices=AssessmentSession.AssessmentType.choices,
        default=AssessmentSession.AssessmentType.COMPREHENSIVE
    )

class AssessmentAnswerItemSerializer(serializers.Serializer):
    question_id = serializers.UUIDField()
    student_answer = serializers.CharField()
    time_taken_seconds = serializers.IntegerField(default=0)

class AssessmentSubmitSerializer(serializers.Serializer):
    answers = serializers.ListField(
        child=AssessmentAnswerItemSerializer()
    )
    time_spent_seconds = serializers.IntegerField(default=0)
