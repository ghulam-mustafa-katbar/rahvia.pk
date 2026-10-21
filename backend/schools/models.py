import uuid
from django.db import models
from django.conf import settings

class School(models.Model):
    class BoardChoice(models.TextChoices):
        FBISE_ISLAMABAD = 'FBISE_ISLAMABAD', 'Federal Board of Intermediate & Secondary Education (FBISE)'
        BISE_LAHORE = 'BISE_LAHORE', 'BISE Lahore'
        BISE_RAWALPINDI = 'BISE_RAWALPINDI', 'BISE Rawalpindi'
        BISE_FAISALABAD = 'BISE_FAISALABAD', 'BISE Faisalabad'
        BISE_MULTAN = 'BISE_MULTAN', 'BISE Multan'
        BISE_GUJRANWALA = 'BISE_GUJRANWALA', 'BISE Gujranwala'
        BISE_SARGODHA = 'BISE_SARGODHA', 'BISE Sargodha'
        BISE_SAHIWAL = 'BISE_SAHIWAL', 'BISE Sahiwal'
        BISE_BAHAWALPUR = 'BISE_BAHAWALPUR', 'BISE Bahawalpur'
        BISE_KARACHI = 'BISE_KARACHI', 'BISE Karachi'
        BISE_HYDERABAD = 'BISE_HYDERABAD', 'BISE Hyderabad'
        BISE_SUKKUR = 'BISE_SUKKUR', 'BISE Sukkur'
        BISE_LARKANA = 'BISE_LARKANA', 'BISE Larkana'
        BISE_PESHAWAR = 'BISE_PESHAWAR', 'BISE Peshawar'
        BISE_ABBOTTABAD = 'BISE_ABBOTTABAD', 'BISE Abbottabad'
        BISE_MARDAN = 'BISE_MARDAN', 'BISE Mardan'
        BISE_SWAT = 'BISE_SWAT', 'BISE Swat'
        BISE_QUETTA = 'BISE_QUETTA', 'BISE Quetta'
        BISE_MIRPUR_AJK = 'BISE_MIRPUR_AJK', 'BISE Mirpur (AJK)'
        CAMBRIDGE_CAIE = 'CAMBRIDGE_CAIE', 'Cambridge CAIE (O/A Levels)'
        OTHER = 'OTHER', 'Other / Autonomous Board'

    class ProvinceChoice(models.TextChoices):
        PUNJAB = 'PUNJAB', 'Punjab'
        SINDH = 'SINDH', 'Sindh'
        KPK = 'KPK', 'Khyber Pakhtunkhwa'
        BALOCHISTAN = 'BALOCHISTAN', 'Balochistan'
        ISLAMABAD = 'ISLAMABAD', 'Islamabad Capital Territory'
        AJK = 'AJK', 'Azad Jammu & Kashmir'
        GILGIT_BALTISTAN = 'GILGIT_BALTISTAN', 'Gilgit-Baltistan'

    school_id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    name = models.CharField(max_length=255)
    code = models.CharField(max_length=50, unique=True, db_index=True, help_text="Unique institution code for student joining")
    board = models.CharField(max_length=50, choices=BoardChoice.choices, default=BoardChoice.FBISE_ISLAMABAD)
    province = models.CharField(max_length=50, choices=ProvinceChoice.choices, default=ProvinceChoice.ISLAMABAD)
    city = models.CharField(max_length=100)
    address = models.TextField(blank=True)
    contact_email = models.EmailField()
    contact_phone = models.CharField(max_length=30, blank=True)
    counselor = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
        related_name='schools'
    )
    verified = models.BooleanField(default=False)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        ordering = ['name']
        verbose_name = 'School / College'
        verbose_name_plural = 'Schools & Colleges'

    def __str__(self):
        return f"{self.name} ({self.city})"
