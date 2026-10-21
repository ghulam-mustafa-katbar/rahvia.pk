import uuid
from django.db import models

class CareerField(models.Model):
    class CategoryChoice(models.TextChoices):
        COMPUTING_AI = 'COMPUTING_AI', 'Computer Science, AI & Software'
        ENGINEERING = 'ENGINEERING', 'Engineering & Technology'
        MEDICAL_HEALTH = 'MEDICAL_HEALTH', 'Medicine, Surgery & Allied Health'
        BUSINESS_FINANCE = 'BUSINESS_FINANCE', 'Business, Finance & Accountancy'
        NATURAL_SCIENCES = 'NATURAL_SCIENCES', 'Natural Sciences & Research'
        SOCIAL_SCIENCES_LAW = 'SOCIAL_SCIENCES_LAW', 'Law, Policy & Social Sciences'
        CREATIVE_MEDIA = 'CREATIVE_MEDIA', 'Creative Arts, Architecture & Media'
        EMERGING_TECH = 'EMERGING_TECH', 'Emerging Tech, Robotics & Space'

    class StreamChoice(models.TextChoices):
        PRE_ENGINEERING = 'PRE_ENGINEERING', 'FSc Pre-Engineering'
        PRE_MEDICAL = 'PRE_MEDICAL', 'FSc Pre-Medical'
        ICS = 'ICS', 'ICS (Computer Science)'
        COMMERCE = 'COMMERCE', 'I.Com / Commerce'
        HUMANITIES = 'HUMANITIES', 'FA / Humanities'
        OPEN_ALL = 'OPEN_ALL', 'Open to Any Intermediate Stream'

    class VerificationStatus(models.TextChoices):
        VERIFIED_OFFICIAL = 'VERIFIED_OFFICIAL', 'Verified from Official Source'
        PARTIALLY_VERIFIED = 'PARTIALLY_VERIFIED', 'Partially Verified'
        NEEDS_VERIFICATION = 'NEEDS_VERIFICATION', 'Needs Verification'
        INSTITUTION_SPECIFIC = 'INSTITUTION_SPECIFIC', 'Institution-Specific Variation'
        OUTDATED = 'OUTDATED', 'Outdated / Needs Update'

    field_id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    name = models.CharField(max_length=200, db_index=True)
    category = models.CharField(max_length=50, choices=CategoryChoice.choices, default=CategoryChoice.COMPUTING_AI)
    description = models.TextField()
    description_urdu = models.TextField(blank=True, help_text="Urdu translation for high accessibility")
    stream_requirement = models.CharField(max_length=50, choices=StreamChoice.choices, default=StreamChoice.OPEN_ALL)
    typical_degrees = models.JSONField(default=list, blank=True, help_text="e.g. ['BS Software Engineering', 'BS Computer Science']")
    required_exams = models.JSONField(default=list, blank=True, help_text="e.g. ['ECAT', 'FAST Test', 'NET (NUST)', 'MDCAT']")
    career_outlook = models.TextField(blank=True, help_text="Industry outlook, salary ranges in PKR, Pakistani market demand")
    related_subjects = models.JSONField(default=list, blank=True, help_text="e.g. ['Mathematics', 'Physics', 'Computer Science']")
    top_universities_pakistan = models.JSONField(default=list, blank=True, help_text="e.g. ['NUST', 'FAST-NU', 'LUMS', 'GIKI', 'UET']")
    
    # Structured Eligibility & Verification Metadata
    structured_eligibility = models.JSONField(
        default=dict,
        blank=True,
        help_text="Detailed eligibility criteria per institution/board: qualification, required subjects, minimum marks, entrance tests"
    )
    verification_status = models.CharField(
        max_length=40,
        choices=VerificationStatus.choices,
        default=VerificationStatus.VERIFIED_OFFICIAL
    )
    official_source_url = models.URLField(max_length=500, blank=True, help_text="Direct link to official HEC/Board/University regulatory page")
    last_verified_date = models.DateField(null=True, blank=True, help_text="Date when admission criteria was verified")
    salary_data = models.JSONField(
        default=dict,
        blank=True,
        help_text="Pakistan-specific salary ranges (entry, mid, senior) with verifiable sources and survey references"
    )

    is_active = models.BooleanField(default=True)
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        ordering = ['name']
        verbose_name = 'Career Field'
        verbose_name_plural = 'Career Fields'

    def __str__(self):
        return f"{self.name} ({self.get_category_display()})"
