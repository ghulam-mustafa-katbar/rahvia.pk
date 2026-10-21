from rest_framework import serializers
from .models import School
from students.models import Student

class SchoolSerializer(serializers.ModelSerializer):
    board_display = serializers.CharField(source='get_board_display', read_only=True)
    province_display = serializers.CharField(source='get_province_display', read_only=True)
    student_count = serializers.IntegerField(source='students.count', read_only=True)

    class Meta:
        model = School
        fields = [
            'school_id', 'name', 'code', 'board', 'board_display',
            'province', 'province_display', 'city', 'address',
            'contact_email', 'contact_phone', 'verified', 'student_count',
            'created_at'
        ]
        read_only_fields = ['school_id', 'created_at']

class SchoolStudentRosterSerializer(serializers.ModelSerializer):
    email = serializers.EmailField(source='user.email', read_only=True)
    grade_display = serializers.CharField(source='get_current_grade_display', read_only=True)
    has_completed_assessment = serializers.SerializerMethodField()
    latest_report_id = serializers.SerializerMethodField()
    top_recommended_stream = serializers.SerializerMethodField()

    class Meta:
        model = Student
        fields = [
            'student_id', 'name', 'email', 'gender', 'board',
            'current_grade', 'grade_display', 'elective_group',
            'parent_consent', 'has_completed_assessment',
            'latest_report_id', 'top_recommended_stream', 'created_at'
        ]

    def get_has_completed_assessment(self, obj):
        return obj.assessments.filter(status='COMPLETED').exists()

    def get_latest_report_id(self, obj):
        report = obj.reports.order_by('-created_at').first()
        return str(report.report_id) if report else None

    def get_top_recommended_stream(self, obj):
        report = obj.reports.order_by('-created_at').first()
        if report and report.recommended_streams:
            return report.recommended_streams[0]
        return None
