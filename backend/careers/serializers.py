from rest_framework import serializers
from .models import CareerField

class CareerFieldSerializer(serializers.ModelSerializer):
    category_display = serializers.CharField(source='get_category_display', read_only=True)
    stream_display = serializers.CharField(source='get_stream_requirement_display', read_only=True)

    class Meta:
        model = CareerField
        fields = [
            'field_id', 'name', 'category', 'category_display',
            'description', 'description_urdu', 'stream_requirement', 'stream_display',
            'typical_degrees', 'required_exams', 'career_outlook',
            'related_subjects', 'top_universities_pakistan',
            'structured_eligibility', 'verification_status',
            'official_source_url', 'last_verified_date', 'salary_data',
            'is_active', 'created_at'
        ]
        read_only_fields = ['field_id', 'created_at']
