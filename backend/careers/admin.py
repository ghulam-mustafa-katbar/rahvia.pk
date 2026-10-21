from django.contrib import admin
from django.utils.html import format_html
from .models import CareerField

@admin.register(CareerField)
class CareerFieldAdmin(admin.ModelAdmin):
    list_display = ('name', 'category_badge', 'stream_badge', 'verification_badge', 'last_verified_date', 'status_badge')
    list_filter = ('category', 'stream_requirement', 'verification_status', 'is_active')
    search_fields = ('name', 'description', 'typical_degrees')
    ordering = ('category', 'name')
    readonly_fields = ('created_at',)
    fieldsets = (
        ('Basic Information & Nomenclature', {
            'fields': ('name', 'category', 'description', 'description_urdu', 'is_active')
        }),
        ('Intermediate Stream & Requirements', {
            'fields': ('stream_requirement', 'typical_degrees', 'required_exams', 'related_subjects')
        }),
        ('Structured Eligibility & Multi-Institution Rules', {
            'description': 'Specific subject combinations, minimum SSC/HSSC marks, and campus variations',
            'fields': ('structured_eligibility',)
        }),
        ('Official Verification & Regulatory Source', {
            'description': 'HEC / PM&DC / PEC / ICAP / University official verification tracking',
            'fields': ('verification_status', 'official_source_url', 'last_verified_date')
        }),
        ('Market Insights & Salary Outlook (Pakistan)', {
            'fields': ('career_outlook', 'salary_data', 'top_universities_pakistan')
        }),
        ('Metadata', {
            'fields': ('created_at',)
        })
    )

    def category_badge(self, obj):
        colors = {
            'COMPUTING_AI': ('#eff6ff', '#1d4ed8'),
            'ENGINEERING': ('#f0fdf4', '#15803d'),
            'MEDICAL_HEALTH': ('#ecfdf5', '#047857'),
            'BUSINESS_FINANCE': ('#fffbeb', '#b45309'),
            'CREATIVE_MEDIA': ('#fdf2f8', '#be185d'),
            'SOCIAL_SCIENCES_LAW': ('#fef2f2', '#b91c1c'),
            'NATURAL_SCIENCES': ('#f5f3ff', '#6d28d9'),
        }
        bg, text = colors.get(obj.category, ('#f1f5f9', '#475569'))
        return format_html(
            '<span style="background:{}; color:{}; padding:3px 8px; border-radius:6px; font-weight:700; font-size:0.75rem;">{}</span>',
            bg, text, obj.get_category_display().split(',')[0]
        )
    category_badge.short_description = 'Field Category'

    def stream_badge(self, obj):
        return format_html(
            '<span style="background:#f8fafc; color:#334155; border:1px solid #cbd5e1; padding:2px 6px; border-radius:4px; font-weight:600; font-size:0.75rem;">{}</span>',
            obj.get_stream_requirement_display()
        )
    stream_badge.short_description = 'Primary Stream'

    def verification_badge(self, obj):
        colors = {
            'VERIFIED_OFFICIAL': ('#dcfce7', '#15803d', '✓ Official Verified'),
            'PARTIALLY_VERIFIED': ('#fef3c7', '#b45309', '⚠️ Partially Verified'),
            'NEEDS_VERIFICATION': ('#fee2e2', '#b91c1c', '❓ Needs Verification'),
            'INSTITUTION_SPECIFIC': ('#e0f2fe', '#0369a1', '🏢 Institution Specific'),
            'OUTDATED': ('#f1f5f9', '#64748b', '⏳ Outdated'),
        }
        bg, text, label = colors.get(obj.verification_status, ('#f1f5f9', '#64748b', obj.verification_status))
        return format_html(
            '<span style="background:{}; color:{}; padding:3px 8px; border-radius:6px; font-weight:700; font-size:0.72rem;">{}</span>',
            bg, text, label
        )
    verification_badge.short_description = 'Verification Status'

    def status_badge(self, obj):
        if obj.is_active:
            return format_html('<span style="color:#16a34a; font-weight:700;">● Active</span>')
        return format_html('<span style="color:#94a3b8; font-weight:600;">○ Inactive</span>')
    status_badge.short_description = 'Status'
