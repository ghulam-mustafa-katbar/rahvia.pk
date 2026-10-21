from rest_framework import serializers
from .models import Student
from schools.models import School

class StudentProfileSerializer(serializers.ModelSerializer):
    email = serializers.EmailField(source='user.email', read_only=True)
    school_name = serializers.CharField(source='school.name', read_only=True)
    school_code = serializers.CharField(write_only=True, required=False, allow_blank=True)

    class Meta:
        model = Student
        fields = [
            'student_id', 'email', 'name', 'dob', 'gender', 'board',
            'current_grade', 'elective_group', 'academic_scores',
            'interests', 'parent_consent', 'school', 'school_name',
            'school_code', 'created_at', 'updated_at'
        ]
        read_only_fields = ['student_id', 'created_at', 'updated_at']

    def update(self, instance, validated_data):
        school_code = validated_data.pop('school_code', None)
        if school_code is not None:
            if school_code.strip():
                school = School.objects.filter(code__iexact=school_code.strip()).first()
                if school:
                    instance.school = school
            else:
                instance.school = None

        return super().update(instance, validated_data)
