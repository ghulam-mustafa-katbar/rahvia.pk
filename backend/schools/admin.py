from django.contrib import admin
from django.utils.html import format_html
from .models import School

@admin.register(School)
class SchoolAdmin(admin.ModelAdmin):
    list_display = ('name', 'code_badge', 'board', 'city', 'province', 'verification_badge', 'student_count', 'created_at')
    list_filter = ('board', 'province', 'verified')
    search_fields = ('name', 'code', 'city', 'contact_email')
    ordering = ('name',)

    def code_badge(self, obj):
        return format_html(
            '<code style="background:#f1f5f9; padding:2px 6px; border-radius:4px; font-weight:700; color:#0f172a;">{}</code>',
            obj.code
        )
    code_badge.short_description = 'School Code'

    def verification_badge(self, obj):
        if obj.verified:
            return format_html('<span style="background:#dcfce7; color:#15803d; padding:2px 8px; border-radius:6px; font-weight:700; font-size:0.75rem;">✓ Verified Partner</span>')
        return format_html('<span style="background:#fef3c7; color:#b45309; padding:2px 8px; border-radius:6px; font-weight:700; font-size:0.75rem;">⏳ Unverified</span>')
    verification_badge.short_description = 'Status'

    def student_count(self, obj):
        count = obj.students.count()
        return format_html('<strong>{}</strong> students', count)
    student_count.short_description = 'Cohort Size'
