from typing import Dict, Any, List, Tuple
from django.db import transaction, models
from assessments.models import AssessmentSession, DimensionScore, Response
from students.models import Student
from careers.models import CareerField
from .models import Report, ReportRecommendation

def evaluate_and_generate_report(assessment: AssessmentSession) -> Report:
    """
    Evidence-grounded recommendation mapping engine for Matric (Class 9-10) students in Sindh, Pakistan.
    Evaluates:
      1. Cognitive Aptitude (Numerical, Logical, Verbal, Spatial, Scientific, Practical Problem Solving)
      2. 6 RIASEC Interest dimensions (Realistic, Investigative, Artistic, Social, Enterprising, Conventional)
      3. 10 Academic Subject Interests (Math, Bio, Physics, Chemistry, CS, Commerce, Social Studies, English, Arts, Tech)
      4. Qualitative career work-style preferences
      5. Self-reported academic strengths and Matric grades

    Maps evidence to:
      - 8 Sindh Class 11 Educational Pathways (SECCAP / Sindh Boards / SBTE) with evidence strength
      - The 8 Pakistan National Career Encyclopedia verified pathways with institutional admission nuances
    """
    student = assessment.student
    dimension_scores = {ds.dimension_name: ds for ds in assessment.dimension_scores.all()}

    def get_score(dim_name: str, fallback: float = 50.0) -> float:
        if dim_name in dimension_scores:
            return float(dimension_scores[dim_name].percentage)
        return fallback

    # 1. Cognitive Aptitude Scores (0 - 100%)
    math_apt = get_score('NumericalAptitude')
    logical_apt = get_score('LogicalReasoning')
    verbal_apt = get_score('VerbalReasoning')
    spatial_apt = get_score('SpatialVisualization')
    scientific_apt = get_score('ScientificReasoning')
    practical_apt = get_score('PracticalProblemSolving')

    # 2. RIASEC Interest Scores (0 - 100%)
    r_realistic = get_score('RIASEC_Realistic')
    r_investigative = get_score('RIASEC_Investigative')
    r_artistic = get_score('RIASEC_Artistic')
    r_social = get_score('RIASEC_Social')
    r_enterprising = get_score('RIASEC_Enterprising')
    r_conventional = get_score('RIASEC_Conventional')

    # 3. Academic Subject Interests from Responses
    academic_interest_map: Dict[str, float] = {}
    responses = Response.objects.filter(
        assessment=assessment
    ).filter(
        models.Q(question__dimension__startswith='Subject_') | 
        models.Q(question__dimension__startswith='Academic_')
    ).select_related('question')
    for r in responses:
        dim = r.question.dimension
        # raw score 1-5 converted to 0-100%
        val = ((float(r.score_awarded) - 1.0) / 4.0) * 100.0
        academic_interest_map[dim] = max(0.0, min(100.0, val))

    int_math = academic_interest_map.get('Subject_Mathematics', academic_interest_map.get('Academic_Math', 50.0))
    int_bio = academic_interest_map.get('Subject_Biology', academic_interest_map.get('Academic_Biology', 50.0))
    int_physics = academic_interest_map.get('Subject_Physics', academic_interest_map.get('Academic_Physics', 50.0))
    int_chem = academic_interest_map.get('Subject_Chemistry', academic_interest_map.get('Academic_Chemistry', 50.0))
    int_cs = academic_interest_map.get('Subject_ComputerScience', academic_interest_map.get('Academic_ComputerScience', 50.0))
    int_commerce = academic_interest_map.get('Subject_Commerce', academic_interest_map.get('Academic_Commerce', 50.0))
    int_social = academic_interest_map.get('Subject_SocialSciences', academic_interest_map.get('Academic_SocialStudies', 50.0))
    int_english = academic_interest_map.get('Subject_Languages', academic_interest_map.get('Academic_EnglishLiterature', 50.0))
    int_arts = academic_interest_map.get('Subject_ArchitectureArt', academic_interest_map.get('Academic_ArtsDrawing', 50.0))
    int_tech = academic_interest_map.get('Subject_TechnicalVocational', academic_interest_map.get('Academic_TechnicalCraft', 50.0))

    # 4. Self-reported academic grades
    academic_scores = student.academic_scores or {}
    math_grade = float(academic_scores.get('Math', 70))
    bio_grade = float(academic_scores.get('Biology', 60))
    physics_grade = float(academic_scores.get('Physics', 65))
    chem_grade = float(academic_scores.get('Chemistry', 65))
    cs_grade = float(academic_scores.get('Computer', academic_scores.get('Computer Science', 70)))

    interests = [str(i).lower() for i in (student.interests or [])]

    # --- 1. Evaluate the 8 Sindh Class 11 Educational Pathways ---
    pathway_evaluations = []

    # 1. Science Pre-Engineering
    eng_score = round(
        0.25 * math_apt +
        0.20 * spatial_apt +
        0.15 * practical_apt +
        0.15 * int_math +
        0.15 * int_physics +
        0.10 * ((math_grade + physics_grade) / 2.0),
        1
    )
    pathway_evaluations.append({
        'stream_name': 'Science Pre-Engineering',
        'stream_name_urdu': 'پری انجینئرنگ (طبیعیات، کیمیا، ریاضی)',
        'fit_score': eng_score,
        'match_strength': 'HIGH_EVIDENCE' if eng_score >= 70 else ('MODERATE_EVIDENCE' if eng_score >= 55 else 'EXPLORATORY'),
        'core_subjects': ['Physics', 'Chemistry', 'Mathematics', 'Urdu Normal / Salees', 'English Normal', 'Pakistan Studies / Islamic Studies'],
        'curriculum_summary': 'Rigorous preparation in differential calculus, mechanics, optics, thermodynamics, and physical chemistry under Sindh Boards (BIEK Karachi, BISE Hyderabad/Sukkur) or AKU-EB.',
        'seccap_criteria': 'Centralized SECCAP Karachi placement cutoff typically 70%–85%+ for top boys and girls colleges (e.g., Adamjee Science College, DJ Science College, St. Joseph\'s College). Minimum eligibility: SSC Science with at least 50% aggregate.',
        'accessible_careers': ['Mechanical & Mechatronics Engineering', 'Electrical & Embedded Systems Engineering', 'Software Engineering & AI', 'Architecture & Spatial Design (NED / NUST)'],
        'rationale_english': f"Your quantitative aptitude ({math_apt:.0f}%), spatial visualization ({spatial_apt:.0f}%), and physics interest align strongly with engineering fundamentals.",
        'rationale_urdu': "ریاضی اور فزکس کے بنیادی اصولوں اور مکینیکل رجحان میں آپ کی مضبوط گرفت پری انجینئرنگ گروپ کے لیے انتہائی موزوں ہے۔"
    })

    # 2. Science Pre-Medical
    med_score = round(
        0.25 * scientific_apt +
        0.20 * int_bio +
        0.15 * int_chem +
        0.15 * r_investigative +
        0.15 * r_social +
        0.10 * bio_grade,
        1
    )
    pathway_evaluations.append({
        'stream_name': 'Science Pre-Medical',
        'stream_name_urdu': 'پری میڈیکل (حیاتیات، طبیعیات، کیمیا)',
        'fit_score': med_score,
        'match_strength': 'HIGH_EVIDENCE' if med_score >= 70 else ('MODERATE_EVIDENCE' if med_score >= 55 else 'EXPLORATORY'),
        'core_subjects': ['Biology (Botany & Zoology)', 'Physics', 'Chemistry', 'Urdu', 'English', 'Islamiat / Pak Studies'],
        'curriculum_summary': 'Intensive focus on cellular biology, genetics, human anatomy, bio-organic chemistry, and physical sciences per Sindh Textbook Board syllabi.',
        'seccap_criteria': 'Highest cutoff in SECCAP Karachi admissions (often 80%–88%+ for premier colleges like Adamjee, DJ, PECHS, St. Lawrence). Minimum PM&DC matric prerequisite is 60% science for eventual medical admissions.',
        'accessible_careers': ['Medicine & Surgery (MBBS / BDS)', 'Biotechnology & Genetic Engineering', 'Pharmacy (Pharm.D)', 'Physical Therapy (DPT)'],
        'rationale_english': f"High scientific reasoning ({scientific_apt:.0f}%), strong investigative interest ({r_investigative:.0f}%), and biological interest ({int_bio:.0f}%) support a demanding clinical pathway.",
        'rationale_urdu': "حیاتیات، کیمسٹری اور انسان دوست خدمت کے شعبوں میں آپ کا شغف پری میڈیکل میں کامیابی کا واضح اشارہ ہے۔"
    })

    # 3. Science General / Computer Science (ICS)
    ics_score = round(
        0.30 * logical_apt +
        0.25 * math_apt +
        0.20 * int_cs +
        0.15 * r_investigative +
        0.10 * cs_grade,
        1
    )
    pathway_evaluations.append({
        'stream_name': 'Science General / Computer Science (ICS)',
        'stream_name_urdu': 'کمپیوٹر سائنس / آئی سی ایس (ریاضی، فزکس/شماریات، کمپیوٹر)',
        'fit_score': ics_score,
        'match_strength': 'HIGH_EVIDENCE' if ics_score >= 70 else ('MODERATE_EVIDENCE' if ics_score >= 55 else 'EXPLORATORY'),
        'core_subjects': ['Mathematics', 'Computer Science (Programming & DB)', 'Physics or Statistics', 'Urdu', 'English', 'Pak Studies'],
        'curriculum_summary': 'Combines mathematical problem solving with programming logic, algorithmic design, and computing hardware under BIEK / Sindh Boards.',
        'seccap_criteria': 'Very high demand in Karachi colleges; SECCAP cutoffs range between 65%–80% for top computer science faculties. Matric Science or General with Math accepted.',
        'accessible_careers': ['Software Engineering & Artificial Intelligence', 'Architecture & Spatial Design (with Physics option)', 'Cybersecurity & Data Science', 'Computing and Information Systems'],
        'rationale_english': f"Logical pattern reasoning ({logical_apt:.0f}%) and quantitative problem solving ({math_apt:.0f}%) demonstrate exceptional software algorithmic readiness.",
        'rationale_urdu': "منطقی سوچ اور کمپیوٹر الگورتھم میں آپ کی قدرتی صلاحیت سافٹ ویئر اور آئی ٹی شعبوں کے لیے شاندار بنیاد ہے۔"
    })

    # 4. Commerce / I.Com
    com_score = round(
        0.25 * math_apt +
        0.20 * verbal_apt +
        0.25 * r_conventional +
        0.15 * r_enterprising +
        0.15 * int_commerce,
        1
    )
    pathway_evaluations.append({
        'stream_name': 'Commerce / I.Com',
        'stream_name_urdu': 'کامرس / آئی کام (اکاؤنٹنگ، معاشیات، بینکاری، تجارت)',
        'fit_score': com_score,
        'match_strength': 'HIGH_EVIDENCE' if com_score >= 70 else ('MODERATE_EVIDENCE' if com_score >= 55 else 'EXPLORATORY'),
        'core_subjects': ['Principles of Accounting', 'Principles of Commerce', 'Commercial Geography / Banking', 'Economics', 'Business Math & Stats'],
        'curriculum_summary': 'Financial record keeping, auditing basics, mercantile commercial laws, macroeconomic concepts, and business mathematics under BIEK Commerce faculty.',
        'seccap_criteria': 'Available across all public and aided commerce colleges in Karachi (e.g., Commecs College, Govt Premier College, Delhi College). Cutoffs range from 50% to 75%+.',
        'accessible_careers': ['Chartered Accountancy & Corporate Finance (ICAP CA / ACCA)', 'Banking & Fintech', 'Corporate Law (via LAT)', 'Business Administration (BBA)'],
        'rationale_english': f"Orderly data handling ({r_conventional:.0f}%), enterprising interest ({r_enterprising:.0f}%), and practical numeracy ({math_apt:.0f}%) match financial governance.",
        'rationale_urdu': "حساب کتاب کی شفافیت، مالیاتی نظم و ضبط اور کاروباری صلاحیت آپ کو کامرس اور چارٹرڈ اکاؤنٹنسی کے لیے موزوں بناتی ہے۔"
    })

    # 5. Humanities / Arts / FA
    art_score = round(
        0.30 * verbal_apt +
        0.20 * r_social +
        0.20 * r_artistic +
        0.15 * int_social +
        0.15 * int_english,
        1
    )
    pathway_evaluations.append({
        'stream_name': 'Humanities / Arts / FA',
        'stream_name_urdu': 'ہیومینٹیز / آرٹس / ایف اے (قانون، نفسیات، صحافت، ادب)',
        'fit_score': art_score,
        'match_strength': 'HIGH_EVIDENCE' if art_score >= 70 else ('MODERATE_EVIDENCE' if art_score >= 55 else 'EXPLORATORY'),
        'core_subjects': ['Civics / Political Science', 'History of Indo-Pak / Islamic History', 'Psychology or Sociology', 'Advanced Literature (English/Urdu/Sindhi)', 'Education'],
        'curriculum_summary': 'Critical discourse, historical analysis, social structures, philosophical principles, and civic governance in Sindh Board arts faculties.',
        'seccap_criteria': 'Open to Matric Science and Arts candidates with passing marks (45%+). Premier institutions like St. Joseph\'s, PECHS Govt Girls College offer rich elective combinations.',
        'accessible_careers': ['Law & Constitutional Advocacy (5-Year LLB via LAT)', 'Architecture & Spatial Design (IVS / NCA design test route)', 'Civil Services (CSS/PCS)', 'Media & Digital Communication'],
        'rationale_english': f"Strong verbal synthesis ({verbal_apt:.0f}%), social empathy ({r_social:.0f}%), and civic curiosity highlight deep potential for legal advocacy and human development.",
        'rationale_urdu': "تحریری اور زبانی ابلاغ کی مہارت، قانونی فہم اور سماجی مسائل میں گہری دلچسپی آپ کو ہیومینٹیز اور قانون کی طرف راغب کرتی ہے۔"
    })

    # 6. Home Economics
    home_score = round(
        0.25 * r_artistic +
        0.25 * practical_apt +
        0.20 * int_arts +
        0.15 * r_social +
        0.15 * scientific_apt,
        1
    )
    pathway_evaluations.append({
        'stream_name': 'Home Economics',
        'stream_name_urdu': 'ہوم اکنامکس (غذائی سائنس، اندرونی تزئین، ٹیکسٹائل)',
        'fit_score': home_score,
        'match_strength': 'HIGH_EVIDENCE' if home_score >= 70 else ('MODERATE_EVIDENCE' if home_score >= 55 else 'EXPLORATORY'),
        'core_subjects': ['Food and Nutrition', 'Textiles and Clothing', 'Art & Interior Architecture', 'Human Development & Family Studies', 'Resource Management'],
        'curriculum_summary': 'Applied science and artistic integration offered at specialized institutions including Rana Liaquat Ali Khan (RLAK) Government College of Home Economics Karachi.',
        'seccap_criteria': 'Specialized admissions directly through RLAK College Karachi and regional colleges. Open to Matric Science and General students.',
        'accessible_careers': ['Interior Architecture & Spatial Design', 'Clinical Nutrition & Dietetics', 'Textile & Apparel Design', 'Early Childhood Development'],
        'rationale_english': f"Creative spatial aesthetics ({r_artistic:.0f}%) and practical design problem solving ({practical_apt:.0f}%) provide a strong foundation for applied life and design sciences.",
        'rationale_urdu': "تخلیقی ڈیزائن، عملی ذہانت اور گھریلو و ماحولیاتی سائنسز میں دلچسپی ہوم اکنامکس کے لیے بہترین امتزاج ہے۔"
    })

    # 7. Medical Technology
    medtech_score = round(
        0.25 * scientific_apt +
        0.25 * practical_apt +
        0.20 * int_bio +
        0.15 * r_realistic +
        0.15 * r_investigative,
        1
    )
    pathway_evaluations.append({
        'stream_name': 'Medical Technology',
        'stream_name_urdu': 'میڈیکل ٹیکنالوجی (لیبارٹری، ریڈیوگرافی، آپریشن تھیٹر)',
        'fit_score': medtech_score,
        'match_strength': 'HIGH_EVIDENCE' if medtech_score >= 70 else ('MODERATE_EVIDENCE' if medtech_score >= 55 else 'EXPLORATORY'),
        'core_subjects': ['Clinical Pathology', 'Hematology & Blood Banking', 'Diagnostic Radiography', 'Microbiology', 'Biomedical Instrumentation'],
        'curriculum_summary': 'Direct clinical-technical skills certified under Sindh Board of Technical Education (SBTE) or affiliated health institutes for high-demand diagnostic support.',
        'seccap_criteria': 'Admissions via SBTE or specialized medical training colleges (e.g., Dow Institute of Medical Technology, Sindh Institute of Physical Medicine). Requires Matric Science with Biology (minimum 50%).',
        'accessible_careers': ['Biotechnology & Genetic Engineering', 'Clinical Laboratory Diagnostics', 'Radiology & Imaging Technology', 'Biomedical Support Services'],
        'rationale_english': f"Hands-on scientific problem solving ({practical_apt:.0f}%) combined with biological curiosity ({int_bio:.0f}%) prepares you for essential clinical diagnostics.",
        'rationale_urdu': "طبی تشخیصی آلات اور عملی سائنسی مہارتوں میں دلچسپی میڈیکل ٹیکنالوجی میں شاندار کیریئر کی ضمانت ہے۔"
    })

    # 8. Technical Stream / DAE
    dae_score = round(
        0.30 * practical_apt +
        0.25 * spatial_apt +
        0.20 * r_realistic +
        0.15 * int_tech +
        0.10 * math_apt,
        1
    )
    pathway_evaluations.append({
        'stream_name': 'Technical Stream / DAE (Associate Engineering)',
        'stream_name_urdu': 'تکنیکی تعلیم / ڈی اے ای (الیکٹریکل، مکینیکل، سول ڈپلومہ)',
        'fit_score': dae_score,
        'match_strength': 'HIGH_EVIDENCE' if dae_score >= 70 else ('MODERATE_EVIDENCE' if dae_score >= 55 else 'EXPLORATORY'),
        'core_subjects': ['Workshop Practice & Machine Shop', 'Engineering Drawing & CAD', 'Electrical Machines / Mechanics', 'Applied Mathematics', 'Applied Chemistry & Physics'],
        'curriculum_summary': '3-year professional engineering diploma under Sindh Board of Technical Education (SBTE), preparing skilled associate engineers with direct industrial and BS Technology progression routes.',
        'seccap_criteria': 'Administered through Sindh Board of Technical Education (SBTE) and Government Colleges of Technology (GCT Karachi, Hyderabad, Sukkur). Requires Matric Science with Physics, Chemistry, Math.',
        'accessible_careers': ['Mechanical & Mechatronics Engineering', 'Electrical & Embedded Systems Engineering', 'Industrial Automation', 'Civil & Structural Technology'],
        'rationale_english': f"High practical troubleshooting ({practical_apt:.0f}%) and realistic mechanical affinity ({r_realistic:.0f}%) make applied technical education a fast-track to engineering mastery.",
        'rationale_urdu': "مشینوں کے ساتھ عملی کام اور فنی مہارتوں میں آپ کی صلاحیت تین سالہ انجینئرنگ ڈپلومہ (DAE) کے لیے بہترین ہے۔"
    })

    # Sort pathways by fit score descending
    pathway_evaluations.sort(key=lambda x: x['fit_score'], reverse=True)
    recommended_stream_names = [p['stream_name'] for p in pathway_evaluations[:3]]

    # --- 2. Strengths and Growth Areas Analysis ---
    strengths = []
    growth_areas = []

    if math_apt >= 75 or logical_apt >= 75:
        strengths.append(f"Strong Quantitative & Logical Reasoning ({max(math_apt, logical_apt):.0f}%): Capable of tackling complex problem structures, deductive proofs, and algebraic abstractions.")
    if verbal_apt >= 75:
        strengths.append(f"High Verbal Reasoning & Textual Synthesis ({verbal_apt:.0f}%): Clear ability to evaluate nuanced reading passages, build structured arguments, and articulate insights.")
    if spatial_apt >= 75:
        strengths.append(f"Acute Spatial Visualization ({spatial_apt:.0f}%): Sharp ability to mentally rotate 3D figures, visualize structural relationships, and interpret schematics.")
    if scientific_apt >= 75:
        strengths.append(f"Scientific Method & Hypothesis Reasoning ({scientific_apt:.0f}%): Strong grasp of empirical inquiry, experimental variables, and natural phenomena.")
    if practical_apt >= 75:
        strengths.append(f"Practical Problem Solving ({practical_apt:.0f}%): Resourceful and pragmatic approach to troubleshooting mechanical and applied dilemmas.")
    if r_investigative >= 75:
        strengths.append("High Investigative Curiosity: Strong internal drive for in-depth research, experimental testing, and finding root causes.")
    if r_enterprising >= 75:
        strengths.append("Strategic & Persuasive Orientation: Natural instinct for project organization, leading peers, and entrepreneurial initiative.")
    if r_artistic >= 75:
        strengths.append("Creative Aesthetics & Design Thinking: Expressive passion for visual balance, conceptual originality, and artistic craft.")

    if not strengths:
        strengths.append("Balanced Multidisciplinary Aptitude: Consistent foundational potential across analytical, communicative, and exploratory learning domains.")

    if math_apt < 60:
        growth_areas.append("Quantitative Foundation: Regular practice with secondary algebra, ratios, and quadratic equations will widen STEM and commerce college admissions.")
    if verbal_apt < 60:
        growth_areas.append("Lexical Breadth & Speed Reading: Reading analytical editorials and bilingual publications will elevate performance in competitive admission tests (LAT, NET, entry exams).")
    if spatial_apt < 60:
        growth_areas.append("Geometric & Diagrammatic Visualisation: Working with geometric proofs and technical drawing sketches will sharpen engineering and spatial aptitude.")
    if scientific_apt < 60:
        growth_areas.append("Experimental Controls & Variable Analysis: Focused review of biology and physics experimental procedures will strengthen scientific reasoning.")

    if not growth_areas:
        growth_areas.append("Competitive Test Strategy: Transition from standard curriculum exercises to timed entrance exam test sets (NET, MDCAT, LAT, ECAT) to optimize speed and precision.")

    # --- 3. Match with Career Fields Catalog (The 8 Verified Pathways) ---
    all_fields = CareerField.objects.filter(is_active=True)
    field_matches: List[Tuple[CareerField, float, str, str]] = []

    for field in all_fields:
        match_score = 0.50
        rationale_reasons = []
        name_lower = field.name.lower()

        if 'architecture' in name_lower:
            match_score = (0.35 * spatial_apt + 0.25 * r_artistic + 0.20 * math_apt + 0.10 * practical_apt + 0.10 * int_arts) / 100.0
            rationale_reasons.append("Outstanding spatial visualization and creative design affinity.")
            rationale_reasons.append("Special Sindh Admission Rule: NED University and NUST require HSSC Mathematics and Physics, while Indus Valley School (IVS) and NCA accept any intermediate stream through their drawing/design aptitude test.")
        elif 'biotechnology' in name_lower:
            match_score = (0.30 * scientific_apt + 0.25 * int_bio + 0.20 * r_investigative + 0.15 * int_chem + 0.10 * logical_apt) / 100.0
            rationale_reasons.append("High investigative aptitude and strong interest in life sciences, molecular genetics, and laboratory research.")
        elif 'accountancy' in name_lower or 'finance' in name_lower:
            match_score = (0.30 * math_apt + 0.25 * r_conventional + 0.20 * r_enterprising + 0.15 * verbal_apt + 0.10 * int_commerce) / 100.0
            rationale_reasons.append("Strong numeracy, structured methodical precision, and commercial awareness aligned with ICAP CA and ACCA.")
        elif 'electrical' in name_lower or 'embedded' in name_lower:
            match_score = (0.30 * math_apt + 0.25 * spatial_apt + 0.20 * practical_apt + 0.15 * r_realistic + 0.10 * int_physics) / 100.0
            rationale_reasons.append("Robust mathematical base, spatial reasoning, and interest in electronic hardware and circuit systems.")
        elif 'law' in name_lower or 'advocacy' in name_lower:
            match_score = (0.40 * verbal_apt + 0.20 * r_social + 0.20 * r_enterprising + 0.10 * logical_apt + 0.10 * int_social) / 100.0
            rationale_reasons.append("High verbal precision, logical synthesis, and social advocacy instincts essential for 5-Year LLB and HEC LAT.")
        elif 'mechanical' in name_lower or 'mechatronics' in name_lower:
            match_score = (0.30 * spatial_apt + 0.25 * practical_apt + 0.20 * math_apt + 0.15 * r_realistic + 0.10 * int_physics) / 100.0
            rationale_reasons.append("Intuitive grasp of 3D mechanisms, physical forces, and hands-on technological troubleshooting.")
        elif 'medicine' in name_lower or 'surgery' in name_lower:
            match_score = (0.25 * scientific_apt + 0.25 * int_bio + 0.20 * r_social + 0.15 * r_investigative + 0.15 * int_chem) / 100.0
            rationale_reasons.append("Exceptional alignment with biomedical inquiry, clinical empathy, and high academic perseverance required for PM&DC MDCAT.")
        elif 'software' in name_lower or 'artificial intelligence' in name_lower:
            match_score = (0.35 * logical_apt + 0.25 * math_apt + 0.20 * int_cs + 0.10 * r_investigative + 0.10 * practical_apt) / 100.0
            rationale_reasons.append("Sharp deductive logic, computational thinking, and software problem-solving orientation.")
        else:
            match_score = (0.25 * logical_apt + 0.25 * math_apt + 0.25 * scientific_apt + 0.25 * verbal_apt) / 100.0
            rationale_reasons.append("General alignment across multidisciplinary analytical domains.")

        # Personal declared interest boost
        if any(w in name_lower or w in field.description.lower() for w in interests):
            match_score = min(0.98, match_score + 0.08)
            rationale_reasons.append("Matches student's personally declared career interest.")

        match_score = max(0.40, min(0.99, round(match_score, 2)))
        rationale_text = " ".join(rationale_reasons)
        rationale_urdu = f"آپ کی قابلیت اور رجحان کے مطابق {field.name} کا شعبہ آپ کی صلاحیتوں کے انتہائی موافق ہے۔"

        field_matches.append((field, match_score, rationale_text, rationale_urdu))

    field_matches.sort(key=lambda x: x[1], reverse=True)

    # --- 4. Synthesize Summary Narrative & Concrete Next Steps (Grade-Specific) ---
    top_stream = pathway_evaluations[0]
    top_stream_name = top_stream['stream_name']
    second_stream_name = pathway_evaluations[1]['stream_name']

    is_class_9 = '9' in str(student.current_grade) or student.current_grade == 'MATRIC_9TH'

    if is_class_9:
        summary_narrative = (
            f"[Stage: Class 9 (SSC Part-I) Foundational Exploration] "
            f"Based on your diagnostic problem-solving assessment, your exploratory profile demonstrates highest affinity for "
            f"{top_stream_name} (Evidence: {top_stream['match_strength'].replace('_', ' ')}), followed by {second_stream_name}. "
            f"As a Class 9 student, your primary goal is foundational skill consolidation in prerequisite subjects before final Matric board examinations. "
            f"Your standout competency is {strengths[0].split(':')[0]}."
        )
        summary_narrative_urdu = (
            f"نہم جماعت (SSC Part-I) کی تعلیمی سطح کے مطابق، آپ کی ذہنی صلاحیتوں اور فطری رجحانات کا سب سے موزوں رخ "
            f"'{top_stream['stream_name_urdu']}' کی جانب اشارہ کرتا ہے۔ "
            f"کلاس 9 کے طالب علم کی حیثیت سے، آپ کا اگلا مرحلہ کلاس 10 میں بنیادی مضامین کو مضبوط بنانا ہے تاکہ انٹرمیڈیٹ میں باآسانی داخلہ ممکن ہو سکے۔"
        )
        next_steps = [
            f"Focus on strengthening core Class 9 syllabus concepts in {', '.join(top_stream['core_subjects'][:3])} to build high cumulative GPA.",
            f"Use this profile as an exploratory guide for Class 10 studies; test different study techniques without premature career foreclosure.",
            f"Explore matching profiles in the Pakistan National Career Encyclopedia to understand degree requirements early.",
            "Discuss these exploratory insights with your teachers to address identified growth areas in your secondary coursework."
        ]
    else:
        summary_narrative = (
            f"[Stage: Class 10 (SSC Part-II) Class 11 Transition & SECCAP Preparation] "
            f"Based on your cognitive aptitude, RIASEC interest profile, and academic subject preferences, your primary "
            f"recommended Class 11 educational pathway is {top_stream_name} (Evidence: {top_stream['match_strength'].replace('_', ' ')}). "
            f"A strong complementary secondary option is {second_stream_name}. "
            f"Your strongest assets include {strengths[0].split(':')[0]}, positioning you effectively for Sindh Board intermediate "
            f"studies and competitive university entry tests."
        )
        summary_narrative_urdu = (
            f"دہم جماعت (SSC Part-II) اور کالج داخلے کی تیاری کے مطابق، جماعت گیارہویں (انٹرمیڈیٹ) کے لیے "
            f"آپ کا سب سے موزوں اور ترجیحی تعلیمی راستہ '{top_stream['stream_name_urdu']}' ہے۔ "
            f"جبکہ متبادل کے طور پر '{pathway_evaluations[1]['stream_name_urdu']}' بھی ایک بہترین انتخاب ہے۔"
        )
        next_steps = [
            f"Prepare for Class 11 centralized admission under SECCAP (Karachi) or relevant Sindh Board (Hyderabad/Sukkur/Larkana) targeting {top_stream_name}.",
            f"Review core prerequisite subjects ({', '.join(top_stream['core_subjects'][:3])}) to ensure high SSC Part-II Matric marks.",
            "Explore recommended career profiles in the Pakistan National Career Encyclopedia to review exact university eligibility criteria and required entry tests.",
            "Discuss this report with your school career counselor or guardian to finalize subject elective selections before college registration."
        ]

    # Snapshots for fast inspection and verifiable reporting
    cognitive_snapshot = {
        'NumericalAptitude': math_apt,
        'LogicalReasoning': logical_apt,
        'VerbalReasoning': verbal_apt,
        'SpatialVisualization': spatial_apt,
        'ScientificReasoning': scientific_apt,
        'PracticalProblemSolving': practical_apt
    }
    riasec_snapshot = {
        'Realistic': r_realistic,
        'Investigative': r_investigative,
        'Artistic': r_artistic,
        'Social': r_social,
        'Enterprising': r_enterprising,
        'Conventional': r_conventional
    }

    # --- 5. Persist Report & Recommendations in Database ---
    with transaction.atomic():
        Report.objects.filter(assessment=assessment).delete()

        report = Report.objects.create(
            assessment=assessment,
            student=student,
            summary_narrative=summary_narrative,
            summary_narrative_urdu=summary_narrative_urdu,
            strengths=strengths,
            growth_areas=growth_areas,
            recommended_streams=recommended_stream_names,
            pathway_details=pathway_evaluations,
            cognitive_scores_snapshot=cognitive_snapshot,
            riasec_scores_snapshot=riasec_snapshot,
            academic_interests_snapshot=academic_interest_map,
            next_steps=next_steps
        )

        recommendation_objs = []
        for rank, (field, score, rationale, rationale_u) in enumerate(field_matches[:6], start=1):
            recommendation_objs.append(ReportRecommendation(
                report=report,
                field=field,
                match_score=score,
                rationale_text=rationale,
                rationale_text_urdu=rationale_u,
                rank=rank
            ))
        ReportRecommendation.objects.bulk_create(recommendation_objs)

    return report
