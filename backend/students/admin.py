from django.contrib import admin
from django.utils.html import format_html
from .models import Student

@admin.register(Student)
class StudentAdmin(admin.ModelAdmin):
    list_display = ('name', 'user_email', 'school_name', 'board_badge', 'grade_badge', 'elective_badge', 'parent_consent_badge', 'created_at')
    list_filter = ('board', 'current_grade', 'elective_group', 'parent_consent')
    search_fields = ('name', 'user__email', 'school__name', 'board')
    ordering = ('-created_at',)

    def user_email(self, obj):
        return obj.user.email
    user_email.short_description = 'Account Email'

    def school_name(self, obj):
        return obj.school.name if obj.school else '—'
    school_name.short_description = 'Institution'

    def board_badge(self, obj):
        return format_html(
            '<span style="background:#f1f5f9; color:#334155; padding:3px 8px; border-radius:6px; font-size:0.75rem; font-weight:600; border:1px solid #cbd5e1;">{}</span>',
            obj.board
        )
    board_badge.short_description = 'Board'

    def grade_badge(self, obj):
        return format_html(
            '<span style="background:#eff6ff; color:#1d4ed8; padding:3px 8px; border-radius:6px; font-size:0.75rem; font-weight:700;">{}</span>',
            obj.current_grade
        )
    grade_badge.short_description = 'Grade Level'

    def elective_badge(self, obj):
        return format_html(
            '<span style="background:#f0fdf4; color:#15803d; padding:3px 8px; border-radius:6px; font-size:0.75rem; font-weight:700;">{}</span>',
            obj.elective_group
        )
    elective_badge.short_description = 'Elective Stream'

    def parent_consent_badge(self, obj):
        if obj.parent_consent:
            return format_html('<span style="color:#16a34a; font-weight:700;">✓ Granted</span>')
        return format_html('<span style="color:#dc2626; font-weight:600;">✗ Required</span>')
    parent_consent_badge.short_description = 'Consent'
