import uuid
from django.db import models
from django.conf import settings
from schools.models import School

class Student(models.Model):
    class GenderChoice(models.TextChoices):
        MALE = 'MALE', 'Male'
        FEMALE = 'FEMALE', 'Female'
        OTHER = 'OTHER', 'Other / Prefer not to say'

    class GradeChoice(models.TextChoices):
        MATRIC_9TH = 'MATRIC_9TH', 'Matric 9th Grade'
        MATRIC_10TH = 'MATRIC_10TH', 'Matric 10th Grade'
        INTER_11TH = 'INTER_11TH', 'Intermediate 1st Year (11th Grade)'
        INTER_12TH = 'INTER_12TH', 'Intermediate 2nd Year (12th Grade)'
        O_LEVELS = 'O_LEVELS', 'Cambridge O-Levels'
        A_LEVELS = 'A_LEVELS', 'Cambridge A-Levels'
        UNDERGRADUATE = 'UNDERGRADUATE', 'Undergraduate / College Entry'

    class ElectiveGroupChoice(models.TextChoices):
        SCIENCE_BIO = 'SCIENCE_BIO', 'Matric Science (Biology)'
        SCIENCE_CS = 'SCIENCE_CS', 'Matric Science (Computer Science)'
        ARTS_GENERAL = 'ARTS_GENERAL', 'Matric Arts / General'
        PRE_ENGINEERING = 'PRE_ENGINEERING', 'FSc Pre-Engineering'
        PRE_MEDICAL = 'PRE_MEDICAL', 'FSc Pre-Medical'
        ICS_CS = 'ICS_CS', 'ICS (Computer Science + Math + Physics/Stats)'
        ICOM = 'ICOM', 'I.Com (Commerce)'
        FA_HUMANITIES = 'FA_HUMANITIES', 'FA (Fine Arts & Humanities)'
        CAMBRIDGE_STEM = 'CAMBRIDGE_STEM', 'Cambridge STEM (Math/Sciences)'
        CAMBRIDGE_PREMED = 'CAMBRIDGE_PREMED', 'Cambridge Pre-Med'
        CAMBRIDGE_BUSINESS = 'CAMBRIDGE_BUSINESS', 'Cambridge Business & Humanities'
        UNDECIDED = 'UNDECIDED', 'Undecided / Exploring Options'

    student_id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    user = models.OneToOneField(
        settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE,
        related_name='student_profile'
    )
    school = models.ForeignKey(
        School,
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
        related_name='students'
    )
    name = models.CharField(max_length=200)
    dob = models.DateField(null=True, blank=True)
    gender = models.CharField(max_length=20, choices=GenderChoice.choices, default=GenderChoice.FEMALE)
    board = models.CharField(max_length=100, default='FBISE Islamabad')
    current_grade = models.CharField(max_length=50, choices=GradeChoice.choices, default=GradeChoice.MATRIC_10TH)
    elective_group = models.CharField(max_length=50, choices=ElectiveGroupChoice.choices, default=ElectiveGroupChoice.SCIENCE_CS)
    academic_scores = models.JSONField(default=dict, blank=True, help_text="e.g. {'Math': 88, 'Physics': 92, 'Chemistry': 85}")
    interests = models.JSONField(default=list, blank=True, help_text="List of interests e.g. ['Robotics', 'Medicine', 'Graphic Design']")
    parent_consent = models.BooleanField(default=False, help_text="Verifiable parental consent for minors per Pakistani PDPA")
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        ordering = ['name']
        verbose_name = 'Student'
        verbose_name_plural = 'Students'

    def __str__(self):
        return f"{self.name} ({self.get_current_grade_display()})"
