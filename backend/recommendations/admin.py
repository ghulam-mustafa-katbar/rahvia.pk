from django.contrib import admin
from django.utils.html import format_html
from .models import Report, ReportRecommendation

class ReportRecommendationInline(admin.TabularInline):
    model = ReportRecommendation
    extra = 0
    readonly_fields = ('field', 'match_score_badge', 'rank', 'rationale_text')
    fields = ('field', 'match_score_badge', 'rank', 'rationale_text')

    def match_score_badge(self, obj):
        pct = float(obj.match_score)
        return format_html(
            '<span style="background:#ecfdf5; color:#047857; font-weight:700; padding:2px 8px; border-radius:6px;">{:.1f}% Match</span>',
            pct
        )
    match_score_badge.short_description = 'Match Score'

@admin.register(Report)
class ReportAdmin(admin.ModelAdmin):
    list_display = ('student', 'recommended_streams_badges', 'top_career_match', 'created_at', 'pdf_action')
    search_fields = ('student__name', 'student__user__email')
    ordering = ('-created_at',)
    inlines = [ReportRecommendationInline]

    def recommended_streams_badges(self, obj):
        badges = [
            f'<span style="background:#eff6ff; color:#1d4ed8; padding:2px 6px; border-radius:4px; font-weight:700; font-size:0.75rem; margin-right:4px;">{stream}</span>'
            for stream in obj.recommended_streams
        ]
        return format_html("".join(badges))
    recommended_streams_badges.short_description = 'Recommended Streams'

    def top_career_match(self, obj):
        first = obj.recommendations.order_by('rank').first()
        if first:
            return format_html('<strong>{}</strong> ({:.0f}%)', first.field.name, first.match_score)
        return "—"
    top_career_match.short_description = 'Top Career Match'

    def pdf_action(self, obj):
        return format_html(
            '<a href="/api/report/{}/pdf" target="_blank" style="background:#059669; color:#fff; padding:3px 10px; border-radius:6px; font-weight:600; font-size:0.75rem; text-decoration:none;">📄 Download PDF</a>',
            obj.report_id
        )
    pdf_action.short_description = 'Dossier Report'


@admin.register(ReportRecommendation)
class ReportRecommendationAdmin(admin.ModelAdmin):
    list_display = ('report', 'field', 'match_score_display', 'rank_badge')
    list_filter = ('rank',)
    search_fields = ('report__student__name', 'field__name')

    def match_score_display(self, obj):
        return f"{obj.match_score:.1f}%"
    match_score_display.short_description = 'Match Score'

    def rank_badge(self, obj):
        return format_html(
            '<span style="background:#f1f5f9; padding:2px 8px; border-radius:4px; font-weight:700;">#{}</span>',
            obj.rank
        )
    rank_badge.short_description = 'Rank'
