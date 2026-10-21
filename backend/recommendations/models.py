import uuid
from django.db import models
from assessments.models import AssessmentSession
from students.models import Student
from careers.models import CareerField

class Report(models.Model):
    report_id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    assessment = models.OneToOneField(
        AssessmentSession,
        on_delete=models.CASCADE,
        related_name='report'
    )
    student = models.ForeignKey(
        Student,
        on_delete=models.CASCADE,
        related_name='reports'
    )
    summary_narrative = models.TextField()
    summary_narrative_urdu = models.TextField(blank=True)
    strengths = models.JSONField(default=list, help_text="List of top strength statements")
    growth_areas = models.JSONField(default=list, help_text="Areas to develop")
    recommended_streams = models.JSONField(default=list, help_text="e.g. ['Pre-Engineering', 'ICS', 'Pre-Medical']")
    pathway_details = models.JSONField(
        default=list,
        blank=True,
        help_text="Detailed Sindh Class 11 educational pathway options with evidence strength, subject combinations, and SECCAP criteria"
    )
    cognitive_scores_snapshot = models.JSONField(default=dict, blank=True, help_text="Snapshot of aptitude dimension scores")
    riasec_scores_snapshot = models.JSONField(default=dict, blank=True, help_text="Snapshot of 6 RIASEC interest scores")
    academic_interests_snapshot = models.JSONField(default=dict, blank=True, help_text="Snapshot of core subject affinities")
    next_steps = models.JSONField(default=list, help_text="Concrete actionable steps for Pakistani education roadmap")
    pdf_report_path = models.CharField(max_length=500, blank=True, null=True)
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        ordering = ['-created_at']
        verbose_name = 'Guidance Report'
        verbose_name_plural = 'Guidance Reports'

    def __str__(self):
        return f"Report for {self.student.name} ({self.created_at.strftime('%Y-%m-%d')})"

class ReportRecommendation(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    report = models.ForeignKey(
        Report,
        on_delete=models.CASCADE,
        related_name='recommendations'
    )
    field = models.ForeignKey(
        CareerField,
        on_delete=models.CASCADE,
        related_name='recommendations'
    )
    match_score = models.FloatField(default=0.0, help_text="Compatibility score between 0.00 and 1.00")
    rationale_text = models.TextField(help_text="Detailed explanation of why student matches this field")
    rationale_text_urdu = models.TextField(blank=True)
    rank = models.IntegerField(default=1)

    class Meta:
        ordering = ['rank', '-match_score']
        verbose_name = 'Report Career Recommendation'
        verbose_name_plural = 'Report Career Recommendations'

    def __str__(self):
        return f"{self.report.student.name} -> {self.field.name} ({self.match_score * 100:.1f}%)"
