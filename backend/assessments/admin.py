from django.contrib import admin
from django.utils.html import format_html
from .models import Question, AssessmentSession, Response, DimensionScore

@admin.register(Question)
class QuestionAdmin(admin.ModelAdmin):
    list_display = ('text_preview', 'urdu_preview', 'category_badge', 'dimension', 'type', 'target_audience', 'active_badge')
    list_filter = ('category', 'dimension', 'type', 'target_audience', 'is_active')
    search_fields = ('text', 'text_urdu', 'dimension')
    ordering = ('category', 'order')

    def text_preview(self, obj):
        return obj.text[:55] + ('...' if len(obj.text) > 55 else '')
    text_preview.short_description = 'Question (EN)'

    def urdu_preview(self, obj):
        if obj.text_urdu:
            return format_html('<span dir="rtl" style="font-family:\'Noto Nastaliq Urdu\', serif; font-size:0.85rem; color:#0f766e;">{}</span>', obj.text_urdu[:40])
        return "—"
    urdu_preview.short_description = 'اردو (Urdu)'

    def category_badge(self, obj):
        colors = {
            'APTITUDE': ('#eff6ff', '#1d4ed8'),
            'INTEREST': ('#f5f3ff', '#6d28d9'),
            'ACADEMIC': ('#ecfdf5', '#047857'),
        }
        bg, text = colors.get(obj.category, ('#f1f5f9', '#475569'))
        return format_html(
            '<span style="background:{}; color:{}; padding:2px 8px; border-radius:6px; font-weight:700; font-size:0.75rem;">{}</span>',
            bg, text, obj.category
        )
    category_badge.short_description = 'Category'

    def active_badge(self, obj):
        if obj.is_active:
            return format_html('<span style="color:#16a34a; font-weight:700;">● Live</span>')
        return format_html('<span style="color:#94a3b8; font-weight:600;">○ Draft</span>')
    active_badge.short_description = 'Status'


@admin.register(AssessmentSession)
class AssessmentSessionAdmin(admin.ModelAdmin):
    list_display = ('student', 'assessment_type', 'status_badge', 'total_score', 'date_taken', 'completed_at')
    list_filter = ('assessment_type', 'status', 'date_taken')
    search_fields = ('student__name', 'student__user__email')
    ordering = ('-date_taken',)

    def status_badge(self, obj):
        colors = {
            'COMPLETED': ('#dcfce7', '#15803d'),
            'IN_PROGRESS': ('#fef3c7', '#b45309'),
            'NOT_STARTED': ('#f1f5f9', '#64748b'),
        }
        bg, text = colors.get(obj.status, ('#f1f5f9', '#64748b'))
        return format_html(
            '<span style="background:{}; color:{}; padding:3px 8px; border-radius:6px; font-weight:700; font-size:0.75rem;">{}</span>',
            bg, text, obj.get_status_display()
        )
    status_badge.short_description = 'Status'


@admin.register(DimensionScore)
class DimensionScoreAdmin(admin.ModelAdmin):
    list_display = ('assessment', 'dimension_name', 'raw_score', 'max_possible', 'percentage_bar', 'percentile')
    list_filter = ('dimension_name',)
    search_fields = ('assessment__student__name', 'dimension_name')

    def percentage_bar(self, obj):
        pct = float(obj.percentage)
        color = '#10b981' if pct >= 70 else ('#3b82f6' if pct >= 50 else '#f59e0b')
        return format_html(
            '''<div style="display:flex; align-items:center; gap:8px;">
                 <div style="width:70px; height:8px; background:#e2e8f0; border-radius:4px; overflow:hidden;">
                   <div style="width:{}%; height:100%; background:{};"></div>
                 </div>
                 <span style="font-weight:700; font-size:0.75rem;">{:.1f}%</span>
               </div>''',
            pct, color, pct
        )
    percentage_bar.short_description = 'Score Ratio'


@admin.register(Response)
class ResponseAdmin(admin.ModelAdmin):
    list_display = ('assessment', 'question_preview', 'student_answer', 'score_awarded', 'created_at')
    search_fields = ('assessment__student__name', 'question__text')

    def question_preview(self, obj):
        return obj.question.text[:40]
    question_preview.short_description = 'Question'
