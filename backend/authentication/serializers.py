from rest_framework import serializers
from rest_framework_simplejwt.tokens import RefreshToken
from django.contrib.auth import authenticate
from django.utils import timezone
from .models import User
from students.models import Student
from schools.models import School

class UserRegistrationSerializer(serializers.ModelSerializer):
    password = serializers.CharField(write_only=True, min_length=6)
    # Student specific optional fields at registration
    name = serializers.CharField(write_only=True, required=False)
    grade = serializers.CharField(write_only=True, required=False, default='MATRIC_10TH')
    board = serializers.CharField(write_only=True, required=False, default='FBISE Islamabad')
    elective_group = serializers.CharField(write_only=True, required=False, default='SCIENCE_CS')
    school_code = serializers.CharField(write_only=True, required=False, allow_blank=True)
    institution_name = serializers.CharField(write_only=True, required=False, allow_blank=True)
    institution_city = serializers.CharField(write_only=True, required=False, allow_blank=True)
    
    # Guardian consent (PDPA compliance)
    parent_guardian_name = serializers.CharField(required=False, allow_blank=True)
    parent_guardian_email = serializers.EmailField(required=False, allow_blank=True)
    parent_guardian_phone = serializers.CharField(required=False, allow_blank=True)
    parent_consent_granted = serializers.BooleanField(required=False, default=False)

    class Meta:
        model = User
        fields = [
            'id', 'email', 'password', 'first_name', 'last_name', 'role',
            'phone_number', 'parent_guardian_name', 'parent_guardian_email',
            'parent_guardian_phone', 'parent_consent_granted',
            'name', 'grade', 'board', 'elective_group', 'school_code',
            'institution_name', 'institution_city'
        ]

    def create(self, validated_data):
        password = validated_data.pop('password')
        name = validated_data.pop('name', '')
        grade = validated_data.pop('grade', 'MATRIC_10TH')
        board = validated_data.pop('board', 'FBISE Islamabad')
        elective_group = validated_data.pop('elective_group', 'SCIENCE_CS')
        school_code = validated_data.pop('school_code', None)
        institution_name = validated_data.pop('institution_name', None)
        institution_city = validated_data.pop('institution_city', None)

        request = self.context.get('request')
        ip_addr = None
        if request:
            ip_addr = request.META.get('HTTP_X_FORWARDED_FOR', request.META.get('REMOTE_ADDR'))
            if ip_addr and ',' in ip_addr:
                ip_addr = ip_addr.split(',')[0].strip()

        if validated_data.get('parent_consent_granted'):
            validated_data['parent_consent_date'] = timezone.now()
            validated_data['parent_consent_ip'] = ip_addr

        user = User.objects.create_user(password=password, **validated_data)

        # If user registered as student, create Student profile automatically
        if user.role == User.Role.STUDENT:
            school = None
            if school_code:
                school = School.objects.filter(code__iexact=school_code.strip()).first()
            
            student_name = name or f"{user.first_name} {user.last_name}".strip() or user.email.split('@')[0]
            Student.objects.create(
                user=user,
                name=student_name,
                school=school,
                board=board,
                current_grade=grade,
                elective_group=elective_group,
                parent_consent=user.parent_consent_granted
            )
        elif user.role == User.Role.COUNSELOR:
            # Associate counselor with their designated institution
            target_school = None
            if school_code:
                target_school = School.objects.filter(code__iexact=school_code.strip()).first()
            if not target_school and institution_name:
                target_school = School.objects.filter(name__iexact=institution_name.strip()).first()
                if not target_school:
                    # Create school record for this new institution
                    base_code = "".join(c for c in institution_name.upper() if c.isalnum())[:8] or "SCH"
                    code_candidate = f"{base_code}-{str(user.id)[:6].upper()}"
                    target_school = School.objects.create(
                        name=institution_name.strip(),
                        code=code_candidate,
                        city=institution_city.strip() if institution_city else 'National',
                        board=board if board else School.BoardChoice.FBISE_ISLAMABAD,
                        contact_email=user.email,
                        verified=False
                    )
            if target_school:
                target_school.counselor = user
                target_school.save()

        return user

class UserLoginSerializer(serializers.Serializer):
    email = serializers.EmailField()
    password = serializers.CharField(write_only=True)

    def validate(self, data):
        email = data.get('email', '').strip().lower()
        password = data.get('password')

        user = authenticate(username=email, password=password)
        if not user:
            raise serializers.ValidationError('Invalid email or password.')

        if not user.is_active:
            raise serializers.ValidationError('Account is suspended or inactive.')

        refresh = RefreshToken.for_user(user)
        return {
            'user': user,
            'access': str(refresh.access_token),
            'refresh': str(refresh),
        }

class UserDetailSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = [
            'id', 'email', 'first_name', 'last_name', 'role', 'phone_number',
            'parent_guardian_name', 'parent_guardian_email', 'parent_guardian_phone',
            'parent_consent_granted', 'parent_consent_date', 'date_joined'
        ]
        read_only_fields = ['id', 'email', 'date_joined', 'parent_consent_date']
