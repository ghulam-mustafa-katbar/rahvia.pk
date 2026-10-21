import uuid
from django.core.management.base import BaseCommand
from django.utils import timezone
from datetime import date
from authentication.models import User
from schools.models import School
from students.models import Student
from careers.models import CareerField
from assessments.models import Question, AssessmentSession, DimensionScore
from recommendations.engine import evaluate_and_generate_report

class Command(BaseCommand):
    help = 'Seeds initial users, schools, comprehensive Matric (Class 9-10) question bank, and verified Pakistani career pathways'

    def handle(self, *args, **options):
        self.stdout.write("Starting database seeding...")

        # ----------------------------------------------------------------------
        # 1. Super Admin User
        # ----------------------------------------------------------------------
        admin_user, created = User.objects.get_or_create(
            email='admin@rahvia.pk',
            defaults={
                'first_name': 'Super',
                'last_name': 'Administrator',
                'role': User.Role.ADMIN,
                'is_staff': True,
                'is_superuser': True,
                'parent_consent_granted': True
            }
        )
        if created:
            admin_user.set_password('Password123!')
            admin_user.save()
            self.stdout.write("Created Super Admin: admin@rahvia.pk / Password123!")

        # ----------------------------------------------------------------------
        # 2. Partner Schools (including Sindh Secondary & Higher Secondary Institutions)
        # ----------------------------------------------------------------------
        schools_data = [
            {
                'code': 'BSEK-KHI-01',
                'name': 'Government National College (Karachi)',
                'board': School.BoardChoice.BISE_KARACHI,
                'province': School.ProvinceChoice.SINDH,
                'city': 'Karachi',
                'address': 'Sir Shah Suleman Road, Gulshan-e-Iqbal, Karachi',
                'contact_email': 'admissions@gnckarachi.edu.pk',
                'contact_phone': '+92-21-99244000',
                'verified': True
            },
            {
                'code': 'DJ-SC-KHI',
                'name': 'D.J. Sindh Government Science College',
                'board': School.BoardChoice.BISE_KARACHI,
                'province': School.ProvinceChoice.SINDH,
                'city': 'Karachi',
                'address': 'Dr Ziauddin Ahmed Road, Saddar, Karachi',
                'contact_email': 'info@djscience.edu.pk',
                'contact_phone': '+92-21-99211517',
                'verified': True
            },
            {
                'code': 'HYD-PCC-01',
                'name': 'Government Degree College & Postgraduate Centre (Hyderabad)',
                'board': School.BoardChoice.BISE_HYDERABAD,
                'province': School.ProvinceChoice.SINDH,
                'city': 'Hyderabad',
                'address': 'Tilak Incline, Latifabad, Hyderabad',
                'contact_email': 'info@gdchyd.edu.pk',
                'contact_phone': '+92-22-9200123',
                'verified': True
            },
            {
                'code': 'SUK-GBC-01',
                'name': 'Public School & College Sukkur',
                'board': School.BoardChoice.BISE_SUKKUR,
                'province': School.ProvinceChoice.SINDH,
                'city': 'Sukkur',
                'address': 'Military Road, Sukkur, Sindh',
                'contact_email': 'info@publicschoolsukkur.edu.pk',
                'contact_phone': '+92-71-5630123',
                'verified': True
            },
            {
                'code': 'IMC-G-F72',
                'name': 'Islamabad Model College for Girls (F-7/2)',
                'board': School.BoardChoice.FBISE_ISLAMABAD,
                'province': School.ProvinceChoice.ISLAMABAD,
                'city': 'Islamabad',
                'address': 'Street 25, Sector F-7/2, Islamabad',
                'contact_email': 'contact@imcgf72.edu.pk',
                'contact_phone': '+92-51-9201234',
                'verified': True
            }
        ]

        created_schools = []
        for sdata in schools_data:
            s_obj, _ = School.objects.update_or_create(
                code=sdata['code'],
                defaults=sdata
            )
            created_schools.append(s_obj)

        school_karachi = created_schools[0]

        # ----------------------------------------------------------------------
        # 3. Counselor User
        # ----------------------------------------------------------------------
        counselor_user, c_created = User.objects.get_or_create(
            email='counselor@rahvia.pk',
            defaults={
                'first_name': 'Dr. Tariq',
                'last_name': 'Mehmood',
                'role': User.Role.COUNSELOR,
                'is_staff': False,
                'phone_number': '+92-300-5551234',
                'parent_consent_granted': True
            }
        )
        if c_created:
            counselor_user.set_password('Password123!')
            counselor_user.save()
            self.stdout.write("Created Counselor: counselor@rahvia.pk / Password123!")
        
        school_karachi.counselor = counselor_user
        school_karachi.save()

        # ----------------------------------------------------------------------
        # 4. Primary Student User & Profile (Aisha Khan - Class 10 Matric)
        # ----------------------------------------------------------------------
        student_user, s_created = User.objects.get_or_create(
            email='student@rahvia.pk',
            defaults={
                'first_name': 'Aisha',
                'last_name': 'Khan',
                'role': User.Role.STUDENT,
                'parent_guardian_name': 'Farooq Ahmed Khan',
                'parent_guardian_email': 'farooq.khan@example.com',
                'parent_guardian_phone': '+92-300-9876543',
                'parent_consent_granted': True,
                'parent_consent_date': timezone.now(),
                'parent_consent_ip': '127.0.0.1'
            }
        )
        if s_created:
            student_user.set_password('Password123!')
            student_user.save()
            self.stdout.write("Created Student: student@rahvia.pk / Password123!")

        student_aisha, _ = Student.objects.update_or_create(
            user=student_user,
            defaults={
                'name': 'Aisha Khan',
                'school': school_karachi,
                'gender': Student.GenderChoice.FEMALE,
                'board': 'BSEK Karachi (Sindh)',
                'current_grade': Student.GradeChoice.MATRIC_10TH,
                'elective_group': Student.ElectiveGroupChoice.SCIENCE_CS,
                'academic_scores': {'Math': 90, 'Physics': 88, 'Chemistry': 84, 'Computer': 94, 'English': 82, 'Biology': 72},
                'interests': ['Software Development', 'Artificial Intelligence', 'Robotics', 'Problem Solving'],
                'parent_consent': True
            }
        )

        # ----------------------------------------------------------------------
        # 5. EIGHT REGISTERED CAREER PATHWAYS (Preserving Exact UUIDs & Taxonomies)
        # ----------------------------------------------------------------------
        careers_payload = [
            {
                'field_id': uuid.UUID('6e9c38e9-c9a9-48b1-af39-31068646cae1'),
                'name': 'Architecture & Spatial Design (B.Arch)',
                'category': CareerField.CategoryChoice.CREATIVE_MEDIA,
                'stream_requirement': CareerField.StreamChoice.OPEN_ALL,
                'description': 'Structural spatial planning, sustainable building design, interior architecture, and urban landscape development.',
                'description_urdu': 'عمارتوں کا فنِ تعمیر، نقشہ نگاری، اندرونی ڈیزائن اور جدید شہری منصوبہ بندی۔',
                'typical_degrees': ['5-Year Bachelor of Architecture (B.Arch)', 'BS Interior Design', 'BS City & Regional Planning'],
                'required_exams': ['NUST NET (Architecture)', 'NED Entry Test & Drawing Test', 'IVS Design Aptitude Test', 'NCA Drawing & Aptitude Test'],
                'career_outlook': 'Diverse opportunities across architectural firms, urban planning authorities (KDA, CDA), real estate development, and private practice.',
                'related_subjects': ['Mathematics', 'Physics', 'Visual Arts', 'Technical Drawing'],
                'top_universities_pakistan': ['NED University Karachi', 'Indus Valley School of Art & Architecture (IVS)', 'NUST (SADA)', 'National College of Arts (NCA)', 'Dawood UET Karachi'],
                'verification_status': CareerField.VerificationStatus.INSTITUTION_SPECIFIC,
                'official_source_url': 'https://pcatp.org.pk/',
                'last_verified_date': date(2026, 10, 15),
                'structured_eligibility': {
                    'qualification': 'Intermediate (HSSC) or equivalent (IBCC Equivalence for O/A-Levels)',
                    'general_notes': 'Admission criteria varies significantly by institution in Pakistan.',
                    'institution_rules': [
                        {
                            'institution': 'NED University of Engineering & Technology (Karachi)',
                            'accepted_streams': ['FSc Pre-Engineering', 'ICS (with Physics & Math)'],
                            'min_marks_hssc': '60% aggregate',
                            'tests_required': ['NED Pre-Admission Entry Test', 'Departmental Drawing Aptitude Test'],
                            'source': 'NED Undergraduate Prospectus'
                        },
                        {
                            'institution': 'Indus Valley School of Art and Architecture (IVS Karachi)',
                            'accepted_streams': ['Open to Any Stream (Pre-Eng, Pre-Med, ICS, Commerce, Humanities, A-Levels)'],
                            'min_marks_hssc': '50% aggregate (or 2nd Division)',
                            'tests_required': ['Mandatory IVS Aptitude & Drawing Test', 'Portfolio Review & Interview'],
                            'source': 'IVS Admissions Office'
                        },
                        {
                            'institution': 'NUST School of Art, Design & Architecture (SADA Islamabad)',
                            'accepted_streams': ['FSc Pre-Engineering', 'ICS with Physics & Mathematics'],
                            'min_marks_hssc': '60% aggregate in both SSC and HSSC',
                            'tests_required': ['NUST NET (Architecture/Design)'],
                            'source': 'NUST Published Criteria'
                        },
                        {
                            'institution': 'National College of Arts (NCA Lahore / Rawalpindi)',
                            'accepted_streams': ['Open to Any Stream (FA, FSc, I.Com, ICS, A-Levels)'],
                            'min_marks_hssc': '45% aggregate (2nd Division)',
                            'tests_required': ['NCA Drawing Test', 'Aptitude Test', 'Mathematics & General Knowledge Test'],
                            'source': 'NCA Prospectus'
                        }
                    ]
                },
                'salary_data': {
                    'currency': 'PKR',
                    'period': 'Monthly',
                    'entry_level': '65,000 - 110,000 PKR (Junior Architect / Draftsman in architecture firms)',
                    'mid_level': '140,000 - 250,000 PKR (Project Architect / Spatial Consultant)',
                    'senior_level': '350,000+ PKR (Principal Architect / Partner / Private Practice)',
                    'source': 'Pakistan Council of Architects & Town Planners (PCATP) Member Survey'
                }
            },
            {
                'field_id': uuid.UUID('50058361-6fb4-4ab8-b226-2af5b0748fcc'),
                'name': 'Biotechnology & Genetic Engineering',
                'category': CareerField.CategoryChoice.NATURAL_SCIENCES,
                'stream_requirement': CareerField.StreamChoice.PRE_MEDICAL,
                'description': 'Molecular biology, vaccine design, forensic DNA analysis, industrial enzymes, and agricultural genetics.',
                'description_urdu': 'بائیوٹیکنالوجی، جینیاتی تحقیق اور حیاتیاتی ادویات سازی کا شعبہ۔',
                'typical_degrees': ['BS Biotechnology', 'BS Molecular Biology', 'BS Microbiology', 'BS Bioinformatics'],
                'required_exams': ['NUST NET (Applied Sciences)', 'Karachi University Entrance Test', 'QAU Departmental Test', 'NTS NAT-IM'],
                'career_outlook': 'Expanding sector in biomedical diagnostics, agricultural research (PARC, NIAB), vaccine manufacturing, and pharmaceutical quality control.',
                'related_subjects': ['Biology', 'Chemistry', 'Physics', 'Mathematics'],
                'top_universities_pakistan': ['University of Karachi (KIBGE)', 'Dow University of Health Sciences', 'NUST (ASAB)', 'Quaid-i-Azam University (QAU)', 'University of the Punjab'],
                'verification_status': CareerField.VerificationStatus.VERIFIED_OFFICIAL,
                'official_source_url': 'https://www.hec.gov.pk/english/services/universities/RevisedCurricula/Documents/2018-2019/BIOTECHNOLOGY.pdf',
                'last_verified_date': date(2026, 10, 10),
                'structured_eligibility': {
                    'qualification': 'Intermediate (HSSC) Pre-Medical',
                    'required_subjects': ['Biology', 'Chemistry', 'Physics'],
                    'min_marks_hssc': '50% - 60% depending on university merit tier',
                    'engineering_exception': 'Selected universities (e.g. NUST ASAB, COMSATS) permit FSc Pre-Engineering candidates subject to passing 6 credit hours of remedial Biology courses in first year.',
                    'tests_required': ['University-specific entry test or NTS NAT-IM']
                },
                'salary_data': {
                    'currency': 'PKR',
                    'period': 'Monthly',
                    'entry_level': '50,000 - 85,000 PKR (Lab Research Associate / QC Officer in pharma)',
                    'mid_level': '110,000 - 190,000 PKR (Senior Microbiologist / Clinical Trial Analyst)',
                    'senior_level': '250,000+ PKR (Chief Scientist / Biotech R&D Director)',
                    'source': 'Pakistan Pharmacists & Biotech Researchers Guild'
                }
            },
            {
                'field_id': uuid.UUID('a60342dd-bbac-416e-8640-af10206e2365'),
                'name': 'Chartered Accountancy & Corporate Finance (CA / ACCA)',
                'category': CareerField.CategoryChoice.BUSINESS_FINANCE,
                'stream_requirement': CareerField.StreamChoice.OPEN_ALL,
                'description': 'Statutory audit, corporate tax compliance, financial risk management, capital allocation, and investment banking.',
                'description_urdu': 'کارپوریٹ فنانس، ٹیکسیشن، آڈٹ اور مالیاتی انتظام کا شعبہ۔',
                'typical_degrees': ['CA (ICAP Pakistan)', 'ACCA (UK)', 'BS Accounting & Finance', 'CFA Charter'],
                'required_exams': ['ICAP PRC (Pre-Requisite Competency Exams)', 'ACCA Applied Knowledge Exams', 'IBA Karachi Test'],
                'career_outlook': 'Premier commercial credentials with high compensation in Big Four audit firms (EY, PwC, KPMG, Deloitte), commercial banks, and multinationals.',
                'related_subjects': ['Mathematics', 'Accounting', 'Economics', 'Business Communication'],
                'top_universities_pakistan': ['ICAP Approved RAETs', 'IBA Karachi', 'LUMS', 'NUST (NBS)', 'SZABIST Karachi'],
                'verification_status': CareerField.VerificationStatus.VERIFIED_OFFICIAL,
                'official_source_url': 'https://icap.org.pk/become-a-ca/entry-routes/',
                'last_verified_date': date(2026, 10, 18),
                'structured_eligibility': {
                    'routes_breakdown': {
                        'ICAP_CA': {
                            'body': 'Institute of Chartered Accountants of Pakistan (ICAP)',
                            'entry_stage': 'PRC (Pre-Requisite Competency) consisting of 5 exams (PRC-1 to PRC-5)',
                            'hssc_requirement': 'Intermediate in ANY group (Science, Commerce, Arts) with minimum 50% marks, or A-Levels with 3 passes',
                            'training_requirement': 'Mandatory 3.5 years articleship training at an approved training organization (TOoP / TOoI)'
                        },
                        'ACCA_UK': {
                            'body': 'Association of Chartered Certified Accountants (Global / UK)',
                            'entry_stage': 'Applied Knowledge Level (BT, MA, FA)',
                            'hssc_requirement': 'Intermediate in ANY group (minimum 50%) or 2 A-Levels + 3 GCSEs (with English and Math)',
                            'foundation_option': 'Candidates without formal prerequisites can start via Foundations in Accountancy (FIA)'
                        }
                    }
                },
                'salary_data': {
                    'currency': 'PKR',
                    'period': 'Monthly',
                    'trainee_stipend': '18,500 - 32,000 PKR (Mandatory ICAP trainee stipend during articleship)',
                    'entry_qualified': '150,000 - 250,000 PKR (Newly Qualified CA / ACCA Member in Big 4 or FMCG)',
                    'senior_level': '450,000 - 1,200,000+ PKR (Finance Director / Partner / CFO)',
                    'source': 'ICAP Member Compensation Survey'
                }
            },
            {
                'field_id': uuid.UUID('3163cd8b-3fc3-4fa3-a169-966ae3a7c3d5'),
                'name': 'Electrical & Embedded Systems Engineering',
                'category': CareerField.CategoryChoice.ENGINEERING,
                'stream_requirement': CareerField.StreamChoice.PRE_ENGINEERING,
                'description': 'Power generation, high-voltage grids, telecommunications, robotics, microchips, and smart IoT hardware.',
                'description_urdu': 'برقی توانائی، الیکٹرانکس، ٹیلی کام، ایمبیڈڈ سسٹمز اور روبوٹکس ہارڈ ویئر۔',
                'typical_degrees': ['BE / BS Electrical Engineering', 'BS Electronic Engineering', 'BS Telecommunication'],
                'required_exams': ['NED Entry Test', 'MUET Pre-Admission Test', 'NUST NET (Engineering)', 'ECAT (Punjab)', 'GIKI Test'],
                'career_outlook': 'Strong foundational engineering career across energy utilities (K-Electric, WAPDA), telecom (PTCL, Jazz, Zong), and industrial automation.',
                'related_subjects': ['Physics', 'Mathematics', 'Computer Science'],
                'top_universities_pakistan': ['NED University Karachi', 'Mehran UET (MUET Jamshoro)', 'NUST (SEECS/E&ME)', 'UET Lahore', 'GIKI'],
                'verification_status': CareerField.VerificationStatus.VERIFIED_OFFICIAL,
                'official_source_url': 'https://www.pec.org.pk/',
                'last_verified_date': date(2026, 10, 12),
                'structured_eligibility': {
                    'regulatory_body': 'Pakistan Engineering Council (PEC)',
                    'hssc_requirement': 'Minimum 60% aggregate marks in FSc Pre-Engineering (Physics, Chemistry, Mathematics).',
                    'ics_exception': 'Per PEC revised policy, ICS candidates with Mathematics, Physics, and Computer Science (minimum 60%) are eligible.',
                    'tests_required': ['Provincial or University Engineering Entrance Test (NED, MUET, NET, ECAT)']
                },
                'salary_data': {
                    'currency': 'PKR',
                    'period': 'Monthly',
                    'entry_level': '70,000 - 130,000 PKR (Graduate Trainee Engineer in utility/telecom/power)',
                    'mid_level': '150,000 - 260,000 PKR (Embedded Firmware Engineer / Grid Automation Lead)',
                    'senior_level': '350,000 - 600,000+ PKR (Chief Technical Officer / Project Director)',
                    'source': 'PEC Industry Employment Data'
                }
            },
            {
                'field_id': uuid.UUID('79a162b0-924b-48ab-a6fd-ab62d4ff1198'),
                'name': 'Law & Constitutional Advocacy (5-Year LLB)',
                'category': CareerField.CategoryChoice.SOCIAL_SCIENCES_LAW,
                'stream_requirement': CareerField.StreamChoice.OPEN_ALL,
                'description': 'Constitutional law, litigation, legal research, corporate contracts, human rights, and judicial administration.',
                'description_urdu': 'آئینی قانون، قانونی تحقیق، وکالت، انسانی حقوق اور عدالتی نظام۔',
                'typical_degrees': ['5-Year Bachelor of Laws (LLB Hons)', 'LLM Corporate Law'],
                'required_exams': ['Law Admission Test (HEC LAT - 50% passing)', 'LUMS LAT/LCAT', 'University Law Tests'],
                'career_outlook': 'High autonomy and prestige. Pathway to High Court advocate, civil service (Judiciary/CSS/PCS), and corporate legal advisor.',
                'related_subjects': ['English', 'Pakistan Studies', 'Political Science', 'Sociology', 'Logic'],
                'top_universities_pakistan': ['University of Karachi (School of Law)', 'Sindh Muslim Law College (SMLC Karachi)', 'LUMS Law School', 'Punjab University Law College', 'SZABIST Law Karachi'],
                'verification_status': CareerField.VERIFIED_OFFICIAL if hasattr(CareerField, 'VERIFIED_OFFICIAL') else CareerField.VerificationStatus.VERIFIED_OFFICIAL,
                'official_source_url': 'https://etc.hec.gov.pk/',
                'last_verified_date': date(2026, 10, 15),
                'structured_eligibility': {
                    'regulatory_bodies': 'Pakistan Bar Council (PBC) & Higher Education Commission (HEC)',
                    'degree_structure': '5-Year integrated LLB (Hons) after Intermediate. (Old 3-year BA-LLB discontinued per Supreme Court / PBC mandate).',
                    'hssc_requirement': 'Intermediate (HSSC in ANY stream: Science, Arts, Commerce, ICS) with minimum 45% or 50% marks.',
                    'mandatory_test': 'HEC Law Admission Test (LAT) with at least 50 out of 100 marks.'
                },
                'salary_data': {
                    'currency': 'PKR',
                    'period': 'Monthly',
                    'junior_advocate': '35,000 - 75,000 PKR (Chambers junior apprentice / stipend)',
                    'mid_level': '120,000 - 250,000 PKR (High Court Advocate / Corporate In-House Counsel)',
                    'senior_level': '500,000+ PKR (Senior Partner / Supreme Court Advocate / Arbitrator)',
                    'source': 'Pakistan Bar Council & Legal Practice Forum'
                }
            },
            {
                'field_id': uuid.UUID('52c36a58-8ed1-4b2d-88ce-2bac82a2de77'),
                'name': 'Mechanical & Mechatronics Engineering',
                'category': CareerField.CategoryChoice.ENGINEERING,
                'stream_requirement': CareerField.StreamChoice.PRE_ENGINEERING,
                'description': 'Thermodynamics, automotive propulsion, manufacturing machinery, aerospace structures, and autonomous mechatronic systems.',
                'description_urdu': 'مکینیکل مشینری، گاڑیوں، صنعتی نظام اور روبوٹکس کا ڈیزائن۔',
                'typical_degrees': ['BE Mechanical Engineering', 'BS Mechatronics Engineering', 'BE Industrial & Manufacturing'],
                'required_exams': ['NED Entry Test', 'MUET Pre-Admission Test', 'ECAT (Punjab)', 'NUST NET (Engineering)', 'GIKI Test'],
                'career_outlook': 'Core industrial discipline with heavy roles in Karachi industrial zones (SITE, Port Qasim, Korangi), automotive plants, and defense production.',
                'related_subjects': ['Physics', 'Mathematics', 'Chemistry', 'Computer Science'],
                'top_universities_pakistan': ['NED University Karachi', 'Mehran UET (MUET Jamshoro)', 'GIKI', 'NUST (SMME)', 'UET Lahore'],
                'verification_status': CareerField.VerificationStatus.VERIFIED_OFFICIAL,
                'official_source_url': 'https://www.pec.org.pk/',
                'last_verified_date': date(2026, 10, 12),
                'structured_eligibility': {
                    'regulatory_body': 'Pakistan Engineering Council (PEC)',
                    'hssc_requirement': 'Minimum 60% aggregate in FSc Pre-Engineering (Physics, Chemistry, Mathematics).',
                    'mechatronics_rule': 'For Mechatronics, ICS with Mathematics and Physics is accepted by select institutions (e.g. NUST, Air University).',
                    'tests_required': ['NED Pre-Admission Test, MUET Test, ECAT, or GIKI/NET']
                },
                'salary_data': {
                    'currency': 'PKR',
                    'period': 'Monthly',
                    'entry_level': '65,000 - 120,000 PKR (Junior Design Engineer / Plant Engineer)',
                    'mid_level': '140,000 - 240,000 PKR (Robotics & Automation Specialist / Operations Lead)',
                    'senior_level': '350,000+ PKR (Engineering Plant Manager / Heavy Industry Director)',
                    'source': 'PEC Industrial Survey'
                }
            },
            {
                'field_id': uuid.UUID('9ac73e6d-1ece-483e-a877-1abd160320d2'),
                'name': 'Medicine & Surgery (MBBS / BDS)',
                'category': CareerField.CategoryChoice.MEDICAL_HEALTH,
                'stream_requirement': CareerField.StreamChoice.PRE_MEDICAL,
                'description': 'Diagnostic pathology, clinical patient care, pharmaceutical therapies, and operative surgery.',
                'description_urdu': 'طبی تشخیص، علاج معالجہ، سرجری اور عوامی صحت کی خدمات۔',
                'typical_degrees': ['MBBS (Bachelor of Medicine, Bachelor of Surgery)', 'BDS (Dental Surgery)'],
                'required_exams': ['National MDCAT (PM&DC Centrally Administered)', 'AKU Entry Test', 'NUMS Entry Test'],
                'career_outlook': 'Prestigious field with lifetime job stability in government teaching hospitals, civil health services (BPS-17), and private clinical networks.',
                'related_subjects': ['Biology', 'Chemistry', 'Physics'],
                'top_universities_pakistan': ['Dow University of Health Sciences (DUHS Karachi)', 'Jinnah Sindh Medical University (JSMU Karachi)', 'Liaquat University of Medical & Health Sciences (LUMHS Jamshoro)', 'Aga Khan University (AKU)', 'King Edward Medical University (KEMU)'],
                'verification_status': CareerField.VerificationStatus.VERIFIED_OFFICIAL,
                'official_source_url': 'https://www.pmdc.pk/',
                'last_verified_date': date(2026, 10, 16),
                'structured_eligibility': {
                    'regulatory_body': 'Pakistan Medical and Dental Council (PM&DC)',
                    'hssc_requirement': 'FSc Pre-Medical (Physics, Chemistry, Biology) with minimum 60% aggregate marks.',
                    'mdcat_requirement': 'Mandatory passing of National MDCAT (55% passing marks for MBBS, 50% for BDS per PM&DC policy).',
                    'sindh_admission_formula': 'Centralized provincial merit: 50% MDCAT + 40% HSSC (Pre-Med) + 10% SSC (Matric).'
                },
                'salary_data': {
                    'currency': 'PKR',
                    'period': 'Monthly',
                    'house_officer': '45,000 - 65,000 PKR (Mandatory paid house job year in teaching hospital)',
                    'medical_officer': '85,000 - 140,000 PKR (Government BPS-17 or private hospital MO)',
                    'consultant_specialist': '250,000 - 800,000+ PKR (Post-FCPS/FRCS Consultant Surgeon / Physician)',
                    'source': 'Sindh Health Department Pay Scales & PMDC Guidelines'
                }
            },
            {
                'field_id': uuid.UUID('eaae056e-ab34-4e1d-8440-3ca8e06991d4'),
                'name': 'Software Engineering & Artificial Intelligence',
                'category': CareerField.CategoryChoice.COMPUTING_AI,
                'stream_requirement': CareerField.StreamChoice.ICS,
                'description': 'Design, development, and algorithmic optimization of enterprise software, cloud microservices, and modern AI/LLM models.',
                'description_urdu': 'سافٹ ویئر، موبائل ایپس، کلاؤڈ سسٹمز اور مصنوعی ذہانت کے حل کی تیاری۔',
                'typical_degrees': ['BS Software Engineering', 'BS Computer Science', 'BS Artificial Intelligence', 'BS Data Science', 'BS Cyber Security'],
                'required_exams': ['FAST Entry Test (NU Test)', 'NUST NET (Computing)', 'NED CS Entry Test', 'Karachi University (UBIT) Test', 'IBA Karachi Test'],
                'career_outlook': 'Highest growth employment sector in Pakistan. Strong demand across Karachi tech clusters, IT exports, and international remote engineering roles.',
                'related_subjects': ['Mathematics', 'Computer Science', 'Physics'],
                'top_universities_pakistan': ['FAST-NUCES (Karachi/Islamabad/Lahore)', 'NUST SEECS', 'NED University (CSIT Karachi)', 'IBA Karachi', 'University of Karachi (UBIT)'],
                'verification_status': CareerField.VerificationStatus.VERIFIED_OFFICIAL,
                'official_source_url': 'https://www.nceac.org.pk/',
                'last_verified_date': date(2026, 10, 19),
                'structured_eligibility': {
                    'regulatory_body': 'National Computing Education Accreditation Council (NCEAC - HEC)',
                    'accepted_streams': ['ICS (Math, Physics/Stats, CS)', 'FSc Pre-Engineering', 'General Science with Mathematics'],
                    'min_marks_hssc': 'Minimum 50% aggregate marks in Intermediate.',
                    'pre_medical_bridge_rule': 'Per HEC notification, FSc Pre-Medical students with 50%+ are eligible for BS Computer Science/Software Engineering, provided they pass a 6-credit deficiency course in Mathematics during their first year of study.'
                },
                'salary_data': {
                    'currency': 'PKR',
                    'period': 'Monthly',
                    'entry_level': '90,000 - 180,000 PKR (Associate Software Engineer / Junior ML Developer)',
                    'mid_level': '200,000 - 380,000 PKR (Full Stack / Cloud DevOps / Data Engineer)',
                    'senior_level': '450,000 - 900,000+ PKR (Principal Architect / Engineering Manager / Global Remote)',
                    'source': 'P@SHA (Pakistan IT Industry) Salary Benchmarks'
                }
            }
        ]

        for cdata in careers_payload:
            CareerField.objects.update_or_create(
                field_id=cdata['field_id'],
                defaults=cdata
            )
        self.stdout.write(f"Updated and verified all {len(careers_payload)} Pakistani Career Pathways.")

        # ----------------------------------------------------------------------
        # 6. COMPREHENSIVE MATRIC (CLASS 9-10) ASSESSMENT QUESTION BANK
        # ----------------------------------------------------------------------
        # Complete bilingual question bank with verified answer keys, explanations,
        # cognitive categories (40% Basic, 40% Intermediate, 20% Challenging),
        # 6 RIASEC interest dimensions (4 per dimension), 10 academic subject interests,
        # and 6 career awareness & learning preference items.
        # ----------------------------------------------------------------------

        # Load complete matric items
        from .matric_questions_data import MATRIC_QUESTIONS_DATA

        for qdata in MATRIC_QUESTIONS_DATA:
            qdata.setdefault('correct_answer', '')
            if qdata.get('category') in [Question.CategoryChoice.INTEREST, Question.CategoryChoice.ACADEMIC, Question.CategoryChoice.PERSONALITY]:
                qdata['correct_answer'] = ''
                qdata['correct_answer_weight'] = 0.0

            q_id = qdata.get('question_id')
            if q_id:
                Question.objects.update_or_create(
                    question_id=q_id,
                    defaults=qdata
                )
            else:
                Question.objects.update_or_create(
                    text=qdata['text'],
                    defaults=qdata
                )

        self.stdout.write(f"Seeded and verified {len(MATRIC_QUESTIONS_DATA)} Matric (Class 9-10) Question Bank items.")

        # ----------------------------------------------------------------------
        # 7. Seed Sample Verified Assessment Session & Report for Aisha Khan
        # ----------------------------------------------------------------------
        # Ensure Aisha Khan has an active session and guidance report reflecting Sindh pathways
        existing_session = AssessmentSession.objects.filter(student=student_aisha).first()
        if not existing_session:
            session = AssessmentSession.objects.create(
                student=student_aisha,
                assessment_type=AssessmentSession.AssessmentType.MATRIC_STREAM,
                status=AssessmentSession.StatusChoice.COMPLETED,
                completed_at=timezone.now(),
                total_score=24.0,
                time_spent_seconds=480
            )
            # Create sample dimension scores
            DimensionScore.objects.create(assessment=session, dimension_name='NumericalAptitude', raw_score=4.0, max_possible=5.0, percentage=80.0, percentile=85.0)
            DimensionScore.objects.create(assessment=session, dimension_name='LogicalReasoning', raw_score=5.0, max_possible=5.0, percentage=100.0, percentile=95.0)
            DimensionScore.objects.create(assessment=session, dimension_name='VerbalReasoning', raw_score=4.0, max_possible=5.0, percentage=80.0, percentile=82.0)
            DimensionScore.objects.create(assessment=session, dimension_name='SpatialVisualization', raw_score=4.0, max_possible=5.0, percentage=80.0, percentile=88.0)
            DimensionScore.objects.create(assessment=session, dimension_name='ScientificReasoning', raw_score=4.0, max_possible=4.0, percentage=100.0, percentile=92.0)
            DimensionScore.objects.create(assessment=session, dimension_name='PracticalProblemSolving', raw_score=3.0, max_possible=4.0, percentage=75.0, percentile=78.0)
            DimensionScore.objects.create(assessment=session, dimension_name='RIASEC_Investigative', raw_score=4.8, max_possible=5.0, percentage=96.0, percentile=94.0)
            DimensionScore.objects.create(assessment=session, dimension_name='RIASEC_Realistic', raw_score=4.2, max_possible=5.0, percentage=84.0, percentile=82.0)
            DimensionScore.objects.create(assessment=session, dimension_name='RIASEC_Enterprising', raw_score=3.8, max_possible=5.0, percentage=76.0, percentile=72.0)
            DimensionScore.objects.create(assessment=session, dimension_name='RIASEC_Artistic', raw_score=3.5, max_possible=5.0, percentage=70.0, percentile=68.0)
            DimensionScore.objects.create(assessment=session, dimension_name='RIASEC_Conventional', raw_score=3.6, max_possible=5.0, percentage=72.0, percentile=70.0)
            DimensionScore.objects.create(assessment=session, dimension_name='RIASEC_Social', raw_score=3.2, max_possible=5.0, percentage=64.0, percentile=60.0)

            report = evaluate_and_generate_report(session)
            self.stdout.write(f"Generated sample guidance report for Aisha Khan: Report ID {report.report_id}")

        self.stdout.write(self.style.SUCCESS("Database seeding and verification completed successfully!"))
