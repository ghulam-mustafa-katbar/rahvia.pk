import uuid
from django.db import models
from students.models import Student

class Question(models.Model):
    class TypeChoice(models.TextChoices):
        MCQ = 'MCQ', 'Multiple Choice Single Answer'
        LIKERT = 'LIKERT', 'Likert Scale (1 to 5)'
        PATTERN = 'PATTERN', 'Pattern / Diagrammatic Logic'
        NUMERICAL = 'NUMERICAL', 'Numerical Calculation'
        VERBAL = 'VERBAL', 'Verbal Comprehension'

    class CategoryChoice(models.TextChoices):
        APTITUDE = 'APTITUDE', 'Cognitive & Academic Aptitude'
        INTEREST = 'INTEREST', 'RIASEC Interest Inventory'
        PERSONALITY = 'PERSONALITY', 'Work Style & Personality'
        ACADEMIC = 'ACADEMIC', 'Core Subject Aptitude'

    class TargetAudienceChoice(models.TextChoices):
        ALL = 'ALL', 'All Grades (Matric & Inter)'
        MATRIC = 'MATRIC', 'Matric (Grade 9-10)'
        INTER = 'INTER', 'Intermediate (Grade 11-12 / A-Levels)'

    class DifficultyChoice(models.TextChoices):
        BASIC = 'BASIC', 'Basic'
        INTERMEDIATE = 'INTERMEDIATE', 'Intermediate'
        CHALLENGING = 'CHALLENGING', 'Challenging'

    question_id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    text = models.TextField()
    text_urdu = models.TextField(blank=True, help_text="Multilingual support in Urdu")
    type = models.CharField(max_length=30, choices=TypeChoice.choices, default=TypeChoice.MCQ)
    category = models.CharField(max_length=30, choices=CategoryChoice.choices, default=CategoryChoice.APTITUDE)
    dimension = models.CharField(
        max_length=80,
        db_index=True,
        help_text="e.g. NumericalAptitude, VerbalReasoning, SpatialVisualization, RIASEC_Realistic, RIASEC_Investigative, etc."
    )
    subcategory = models.CharField(max_length=80, blank=True, help_text="e.g. MentalRotation, Proportions, Mechanics")
    difficulty = models.CharField(max_length=20, choices=DifficultyChoice.choices, default=DifficultyChoice.INTERMEDIATE)
    target_audience = models.CharField(max_length=30, choices=TargetAudienceChoice.choices, default=TargetAudienceChoice.ALL)
    options = models.JSONField(
        default=list,
        help_text="List of choices: [{'id': 'A', 'text': '...', 'text_urdu': '...', 'score': 1.0}]"
    )
    correct_answer = models.CharField(max_length=50, blank=True, help_text="Identifier of the correct option for cognitive tests")
    correct_answer_weight = models.FloatField(default=1.0)
    explanation = models.TextField(blank=True, help_text="Step-by-step mathematical/logical explanation of the answer")
    explanation_urdu = models.TextField(blank=True, help_text="Urdu translation of the solution explanation")
    is_reverse_scored = models.BooleanField(default=False, help_text="True if Likert scale scoring is inverted (5 -> 1)")
    order = models.IntegerField(default=0)
    is_active = models.BooleanField(default=True)
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        ordering = ['order', 'created_at']
        verbose_name = 'Question'
        verbose_name_plural = 'Questions'

    def __str__(self):
        return f"[{self.category}] {self.dimension}: {self.text[:50]}..."

class AssessmentSession(models.Model):
    class StatusChoice(models.TextChoices):
        IN_PROGRESS = 'IN_PROGRESS', 'In Progress'
        COMPLETED = 'COMPLETED', 'Completed'
        ABANDONED = 'ABANDONED', 'Abandoned'

    class AssessmentType(models.TextChoices):
        MATRIC_STREAM = 'MATRIC_STREAM', 'Matric Stream Selection (9th/10th)'
        INTER_CAREER = 'INTER_CAREER', 'Intermediate Career & Degree Pathway (11th/12th)'
        COMPREHENSIVE = 'COMPREHENSIVE', 'Comprehensive Aptitude & Interest Inventory'

    assessment_id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    student = models.ForeignKey(Student, on_delete=models.CASCADE, related_name='assessments')
    assessment_type = models.CharField(max_length=50, choices=AssessmentType.choices, default=AssessmentType.COMPREHENSIVE)
    status = models.CharField(max_length=30, choices=StatusChoice.choices, default=StatusChoice.IN_PROGRESS)
    date_taken = models.DateTimeField(auto_now_add=True)
    completed_at = models.DateTimeField(null=True, blank=True)
    total_score = models.FloatField(default=0.0)
    time_spent_seconds = models.IntegerField(default=0)
    comments = models.TextField(blank=True)

    class Meta:
        ordering = ['-date_taken']
        verbose_name = 'Assessment Session'
        verbose_name_plural = 'Assessment Sessions'

    def __str__(self):
        return f"{self.student.name} - {self.get_assessment_type_display()} ({self.status})"

class Response(models.Model):
    response_id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    assessment = models.ForeignKey(AssessmentSession, on_delete=models.CASCADE, related_name='responses')
    question = models.ForeignKey(Question, on_delete=models.CASCADE, related_name='responses')
    student_answer = models.CharField(max_length=100)
    score_awarded = models.FloatField(default=0.0)
    time_taken_seconds = models.IntegerField(default=0)
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        unique_together = ('assessment', 'question')
        verbose_name = 'Student Response'
        verbose_name_plural = 'Student Responses'

    def __str__(self):
        return f"{self.assessment.student.name} - Q: {self.question_id} (Score: {self.score_awarded})"

class DimensionScore(models.Model):
    score_id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    assessment = models.ForeignKey(AssessmentSession, on_delete=models.CASCADE, related_name='dimension_scores')
    dimension_name = models.CharField(max_length=100, db_index=True)
    raw_score = models.FloatField(default=0.0)
    max_possible = models.FloatField(default=0.0)
    percentage = models.FloatField(default=0.0)
    percentile = models.FloatField(default=50.0, help_text="Norm-referenced or cohort-relative percentile rank")

    class Meta:
        unique_together = ('assessment', 'dimension_name')
        ordering = ['-percentage']
        verbose_name = 'Dimension Score'
        verbose_name_plural = 'Dimension Scores'

    def __str__(self):
        return f"{self.dimension_name}: {self.percentage:.1f}% ({self.percentile:.1f}th %ile)"
