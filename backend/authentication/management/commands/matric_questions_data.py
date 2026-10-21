import uuid
from assessments.models import Question

# ==============================================================================
# RAHVIA PLATFORM — MATRIC (CLASS 9-10) STANDARDIZED ASSESSMENT BLUEPRINT
# Audited, age-appropriate (ages 14-16), bilingual (English & Urdu)
# Preserves historical UUIDs and conforms to educational psychometric standards.
# ==============================================================================

MATRIC_QUESTIONS_DATA = [
    # ==========================================================================
    # SECTION 1: COGNITIVE APTITUDE (28 ITEMS)
    # Target: 40% Basic, 40% Intermediate, 20% Challenging
    # ==========================================================================

    # --- A. NUMERICAL APTITUDE (5 Items) ---
    {
        'question_id': uuid.UUID('81bc6a50-9597-4baa-bef3-5c8b68c1cbc9'),
        'text': 'A student scores 360 marks out of 450 in an annual examination. What is the student\'s percentage score?',
        'text_urdu': 'ایک طالب علم سالانہ امتحان میں 450 میں سے 360 نمبر حاصل کرتا ہے۔ طالب علم کے حاصل کردہ نمبروں کی فیصد کتنی ہے؟',
        'type': Question.TypeChoice.MCQ,
        'category': Question.CategoryChoice.APTITUDE,
        'dimension': 'NumericalAptitude',
        'subcategory': 'Percentages',
        'difficulty': Question.DifficultyChoice.BASIC,
        'target_audience': Question.TargetAudienceChoice.MATRIC,
        'order': 1,
        'correct_answer': 'C',
        'correct_answer_weight': 1.0,
        'explanation': 'Percentage = (360 / 450) * 100 = 0.8 * 100 = 80%.',
        'explanation_urdu': 'فیصد = (360 تقسیم 450) ضرب 100 = 80 فیصد۔',
        'options': [
            {'id': 'A', 'text': '70%', 'text_urdu': '70%'},
            {'id': 'B', 'text': '75%', 'text_urdu': '75%'},
            {'id': 'C', 'text': '80%', 'text_urdu': '80%'},
            {'id': 'D', 'text': '85%', 'text_urdu': '85%'}
        ]
    },
    {
        'question_id': uuid.UUID('ce432bb3-db0e-4363-84f9-8294a5acff74'),
        'text': 'A train traveling at 72 km/h crosses a 200-meter long railway platform in 25 seconds. What is the length of the train?',
        'text_urdu': 'ایک ریل گاڑی جو 72 کلومیٹر فی گھنٹہ کی رفتار سے چل رہی ہے، 200 میٹر لمبے پلیٹ فارم کو 25 سیکنڈ میں عبور کرتی ہے۔ گاڑی کی لمبائی کتنی ہے؟',
        'type': Question.TypeChoice.MCQ,
        'category': Question.CategoryChoice.APTITUDE,
        'dimension': 'NumericalAptitude',
        'subcategory': 'SpeedTimeDistance',
        'difficulty': Question.DifficultyChoice.INTERMEDIATE,
        'target_audience': Question.TargetAudienceChoice.MATRIC,
        'order': 2,
        'correct_answer': 'C',
        'correct_answer_weight': 1.0,
        'explanation': 'Speed in m/s = 72 * (1000 / 3600) = 20 m/s. Total distance in 25s = 20 * 25 = 500 m. Train length = 500 - 200 = 300 meters.',
        'explanation_urdu': 'رفتار میٹر فی سیکنڈ میں = 72 ضرب (1000/3600) = 20 میٹر/سیکنڈ۔ کل فاصلہ = 20 ضرب 25 = 500 میٹر۔ ریل گاڑی کی لمبائی = 500 - 200 = 300 میٹر۔',
        'options': [
            {'id': 'A', 'text': '250 meters', 'text_urdu': '250 میٹر'},
            {'id': 'B', 'text': '280 meters', 'text_urdu': '280 میٹر'},
            {'id': 'C', 'text': '300 meters', 'text_urdu': '300 میٹر'},
            {'id': 'D', 'text': '350 meters', 'text_urdu': '350 میٹر'}
        ]
    },
    {
        'question_id': uuid.UUID('e8f89b26-cb2a-492b-a2ca-7598553e0379'),
        'text': 'If f(x) = 2x² - 3x + 5, what is the value of f(4) - f(2)?',
        'text_urdu': 'اگر f(x) = 2x² - 3x + 5 ہو، تو f(4) - f(2) کی قیمت کیا ہوگی؟',
        'type': Question.TypeChoice.MCQ,
        'category': Question.CategoryChoice.APTITUDE,
        'dimension': 'NumericalAptitude',
        'subcategory': 'AlgebraicFunctions',
        'difficulty': Question.DifficultyChoice.INTERMEDIATE,
        'target_audience': Question.TargetAudienceChoice.MATRIC,
        'order': 3,
        'correct_answer': 'B',
        'correct_answer_weight': 1.0,
        'explanation': 'f(4) = 2(16) - 12 + 5 = 25. f(2) = 2(4) - 6 + 5 = 7. Difference = 25 - 7 = 18.',
        'explanation_urdu': 'f(4) = 2(16) - 12 + 5 = 25. f(2) = 2(4) - 6 + 5 = 7. فرق = 25 - 7 = 18۔',
        'options': [
            {'id': 'A', 'text': '16', 'text_urdu': '16'},
            {'id': 'B', 'text': '18', 'text_urdu': '18'},
            {'id': 'C', 'text': '22', 'text_urdu': '22'},
            {'id': 'D', 'text': '25', 'text_urdu': '25'}
        ]
    },
    {
        'question_id': uuid.UUID('7b19a101-1111-4000-8000-000000000001'),
        'text': 'A recipe serving 8 people requires 300 grams of flour. How many grams of flour are required to prepare the same recipe for 12 people?',
        'text_urdu': '8 افراد کے لیے کھانے کی ترکیب میں 300 گرام آٹے کی ضرورت ہوتی ہے۔ اسی تناسب سے 12 افراد کے لیے کتنے گرام آٹے کی ضرورت ہوگی؟',
        'type': Question.TypeChoice.MCQ,
        'category': Question.CategoryChoice.APTITUDE,
        'dimension': 'NumericalAptitude',
        'subcategory': 'Proportions',
        'difficulty': Question.DifficultyChoice.BASIC,
        'target_audience': Question.TargetAudienceChoice.MATRIC,
        'order': 4,
        'correct_answer': 'B',
        'correct_answer_weight': 1.0,
        'explanation': 'Amount per person = 300 / 8 = 37.5g. For 12 people = 37.5 * 12 = 450 grams.',
        'explanation_urdu': 'فی کس ضرورت = 300 تقسیم 8 = 37.5 گرام۔ 12 افراد کے لیے = 37.5 ضرب 12 = 450 گرام۔',
        'options': [
            {'id': 'A', 'text': '400 grams', 'text_urdu': '400 گرام'},
            {'id': 'B', 'text': '450 grams', 'text_urdu': '450 گرام'},
            {'id': 'C', 'text': '480 grams', 'text_urdu': '480 گرام'},
            {'id': 'D', 'text': '500 grams', 'text_urdu': '500 گرام'}
        ]
    },
    {
        'question_id': uuid.UUID('7b19a101-1111-4000-8000-000000000002'),
        'text': 'A science textbook with an original retail price of 1,500 PKR is offered at a 20% promotional discount. What is the discounted selling price?',
        'text_urdu': 'ایک سائنسی کتاب کی اصل قیمت 1,500 روپے ہے۔ اگر اس پر 20 فیصد رعایت دی جائے، تو کتاب کی فروخت کی قیمت کیا ہوگی؟',
        'type': Question.TypeChoice.MCQ,
        'category': Question.CategoryChoice.APTITUDE,
        'dimension': 'NumericalAptitude',
        'subcategory': 'CommercialMath',
        'difficulty': Question.DifficultyChoice.BASIC,
        'target_audience': Question.TargetAudienceChoice.MATRIC,
        'order': 5,
        'correct_answer': 'A',
        'correct_answer_weight': 1.0,
        'explanation': 'Discount = 20% of 1500 = 300 PKR. Selling price = 1500 - 300 = 1,200 PKR.',
        'explanation_urdu': 'رعایت = 1500 کا 20 فیصد = 300 روپے۔ قیمتِ فروخت = 1500 - 300 = 1,200 روپے۔',
        'options': [
            {'id': 'A', 'text': '1,200 PKR', 'text_urdu': '1,200 روپے'},
            {'id': 'B', 'text': '1,250 PKR', 'text_urdu': '1,250 روپے'},
            {'id': 'C', 'text': '1,300 PKR', 'text_urdu': '1,300 روپے'},
            {'id': 'D', 'text': '1,350 PKR', 'text_urdu': '1,350 روپے'}
        ]
    },

    # --- B. LOGICAL REASONING (5 Items) ---
    {
        'question_id': uuid.UUID('6c36347f-ad09-48f6-81a6-feca1c65046e'),
        'text': 'Complete the number series: 2, 6, 12, 20, 30, ___?',
        'text_urdu': 'اعداد کے سلسلے کو مکمل کریں: 2، 6، 12، 20، 30، ___؟',
        'type': Question.TypeChoice.MCQ,
        'category': Question.CategoryChoice.APTITUDE,
        'dimension': 'LogicalReasoning',
        'subcategory': 'SeriesPatterns',
        'difficulty': Question.DifficultyChoice.BASIC,
        'target_audience': Question.TargetAudienceChoice.MATRIC,
        'order': 6,
        'correct_answer': 'C',
        'correct_answer_weight': 1.0,
        'explanation': 'Differences between consecutive numbers increase by 2: +4, +6, +8, +10, +12. 30 + 12 = 42.',
        'explanation_urdu': 'مسلسل اعداد کے درمیان فرق میں 2 کا اضافہ ہو رہا ہے: +4، +6، +8، +10، +12۔ لہٰذا 30 + 12 = 42۔',
        'options': [
            {'id': 'A', 'text': '36', 'text_urdu': '36'},
            {'id': 'B', 'text': '40', 'text_urdu': '40'},
            {'id': 'C', 'text': '42', 'text_urdu': '42'},
            {'id': 'D', 'text': '44', 'text_urdu': '44'}
        ]
    },
    {
        'question_id': uuid.UUID('118130c4-2fda-4603-aa39-c765e1ec9aac'),
        'text': 'Complete the logical progression: 3, 7, 15, 31, 63, ... ?',
        'text_urdu': 'منطقی تسلسل کو مکمل کریں: 3، 7، 15، 31، 63، ... ؟',
        'type': Question.TypeChoice.MCQ,
        'category': Question.CategoryChoice.APTITUDE,
        'dimension': 'LogicalReasoning',
        'subcategory': 'SeriesPatterns',
        'difficulty': Question.DifficultyChoice.INTERMEDIATE,
        'target_audience': Question.TargetAudienceChoice.MATRIC,
        'order': 7,
        'correct_answer': 'B',
        'correct_answer_weight': 1.0,
        'explanation': 'Pattern is n * 2 + 1: 3*2+1=7; 7*2+1=15; 15*2+1=31; 31*2+1=63; 63*2+1=127.',
        'explanation_urdu': 'اصول یہ ہے کہ عدد کو 2 سے ضرب دے کر 1 جمع کریں: 63 ضرب 2 جمع 1 = 127۔',
        'options': [
            {'id': 'A', 'text': '125', 'text_urdu': '125'},
            {'id': 'B', 'text': '127', 'text_urdu': '127'},
            {'id': 'C', 'text': '129', 'text_urdu': '129'},
            {'id': 'D', 'text': '131', 'text_urdu': '131'}
        ]
    },
    {
        'question_id': uuid.UUID('7b19a101-1111-4000-8000-000000000003'),
        'text': 'Consider the rule: "Whenever it rains, the football field becomes muddy." Today, the football field is completely dry. What is the most logically certain conclusion?',
        'text_urdu': 'اس بیان پر غور کریں: "جب بھی بارش ہوتی ہے، فٹ بال کا گراؤنڈ کیچڑ زدہ ہو جاتا ہے۔" آج گراؤنڈ بالکل خشک ہے۔ منطقی طور پر کیا نتیجہ اخذ کیا جا سکتا ہے؟',
        'type': Question.TypeChoice.MCQ,
        'category': Question.CategoryChoice.APTITUDE,
        'dimension': 'LogicalReasoning',
        'subcategory': 'ConditionalLogic',
        'difficulty': Question.DifficultyChoice.INTERMEDIATE,
        'target_audience': Question.TargetAudienceChoice.MATRIC,
        'order': 8,
        'correct_answer': 'C',
        'correct_answer_weight': 1.0,
        'explanation': 'By Modus Tollens: If P then Q. Not Q, therefore Not P. The field is dry, so it did not rain.',
        'explanation_urdu': 'منطقی اصول کے مطابق: اگر بارش سے گراؤنڈ گیلا ہوتا ہے، اور گراؤنڈ خشک ہے تو لازماً بارش نہیں ہوئی۔',
        'options': [
            {'id': 'A', 'text': 'It rained lightly in the morning.', 'text_urdu': 'صبح ہلکی بارش ہوئی تھی۔'},
            {'id': 'B', 'text': 'The field was covered with a sheet.', 'text_urdu': 'گراؤنڈ کو ترپال سے ڈھانپ دیا گیا تھا۔'},
            {'id': 'C', 'text': 'It did not rain.', 'text_urdu': 'یقیناً بارش نہیں ہوئی۔'},
            {'id': 'D', 'text': 'No conclusion can be drawn.', 'text_urdu': 'کوئی حتمی نتیجہ نہیں نکالا جا سکتا۔'}
        ]
    },
    {
        'question_id': uuid.UUID('7b19a101-1111-4000-8000-000000000004'),
        'text': 'In a single line of 25 students, Tariq is ranked 8th from the front. What is his position counting from the back of the line?',
        'text_urdu': '25 طلباء کی ایک سیدھی قطار میں طارق کا نمبر آگے سے 8 واں ہے۔ قطار کے پیچھے سے گننے پر اس کا نمبر کیا ہوگا؟',
        'type': Question.TypeChoice.MCQ,
        'category': Question.CategoryChoice.APTITUDE,
        'dimension': 'LogicalReasoning',
        'subcategory': 'RankingOrder',
        'difficulty': Question.DifficultyChoice.INTERMEDIATE,
        'target_audience': Question.TargetAudienceChoice.MATRIC,
        'order': 9,
        'correct_answer': 'B',
        'correct_answer_weight': 1.0,
        'explanation': 'Position from back = (Total students - Position from front) + 1 = (25 - 8) + 1 = 18th.',
        'explanation_urdu': 'پیچھے سے پوزیشن = (کل طلباء - آگے سے پوزیشن) + 1 = (25 - 8) + 1 = 18 واں۔',
        'options': [
            {'id': 'A', 'text': '17th', 'text_urdu': '17 واں'},
            {'id': 'B', 'text': '18th', 'text_urdu': '18 واں'},
            {'id': 'C', 'text': '19th', 'text_urdu': '19 واں'},
            {'id': 'D', 'text': '20th', 'text_urdu': '20 واں'}
        ]
    },
    {
        'question_id': uuid.UUID('7b19a101-1111-4000-8000-000000000005'),
        'text': 'Find the next term in the alphanumeric pattern: A2, C4, E8, G16, ___?',
        'text_urdu': 'حروف اور اعداد کے اس نمونے میں اگلی اصطلاح تلاش کریں: A2, C4, E8, G16, ___؟',
        'type': Question.TypeChoice.MCQ,
        'category': Question.CategoryChoice.APTITUDE,
        'dimension': 'LogicalReasoning',
        'subcategory': 'MatrixReasoning',
        'difficulty': Question.DifficultyChoice.CHALLENGING,
        'target_audience': Question.TargetAudienceChoice.MATRIC,
        'order': 10,
        'correct_answer': 'D',
        'correct_answer_weight': 1.0,
        'explanation': 'Letters skip one: A(+2)->C(+2)->E(+2)->G(+2)->I. Numbers double: 2, 4, 8, 16, 32. Result = I32.',
        'explanation_urdu': 'حروف ایک چھوڑ کر آگے بڑھتے ہیں (A, C, E, G کے بعد I)، اور اعداد دوگنے ہو رہے ہیں (16 کے بعد 32)۔ لہٰذا درست جواب I32 ہے۔',
        'options': [
            {'id': 'A', 'text': 'H24', 'text_urdu': 'H24'},
            {'id': 'B', 'text': 'H32', 'text_urdu': 'H32'},
            {'id': 'C', 'text': 'I24', 'text_urdu': 'I24'},
            {'id': 'D', 'text': 'I32', 'text_urdu': 'I32'}
        ]
    },

    # --- C. VERBAL REASONING (5 Items) ---
    {
        'question_id': uuid.UUID('a6ad88e0-ed01-4389-9dae-89446f6e2cbb'),
        'text': 'Choose the word closest in meaning (synonym) to: "ACCURATE".',
        'text_urdu': 'لفظ "ACCURATE" (درست/صحیح) کا ہم معنی لفظ منتخب کریں۔',
        'type': Question.TypeChoice.MCQ,
        'category': Question.CategoryChoice.APTITUDE,
        'dimension': 'VerbalReasoning',
        'subcategory': 'Synonyms',
        'difficulty': Question.DifficultyChoice.BASIC,
        'target_audience': Question.TargetAudienceChoice.MATRIC,
        'order': 11,
        'correct_answer': 'B',
        'correct_answer_weight': 1.0,
        'explanation': 'Accurate means free from error or exact, which is synonymous with Precise.',
        'explanation_urdu': 'Accurate کا مطلب ہے بنا غلطی کے، یعنی Precise (درست یا ٹھیک)۔',
        'options': [
            {'id': 'A', 'text': 'Incorrect', 'text_urdu': 'غلط'},
            {'id': 'B', 'text': 'Precise', 'text_urdu': 'درست و واضح (Precise)'},
            {'id': 'C', 'text': 'Careless', 'text_urdu': 'لاپرواہ'},
            {'id': 'D', 'text': 'Uncertain', 'text_urdu': 'غیر یقینی'}
        ]
    },
    {
        'question_id': uuid.UUID('180c0126-8fda-4b35-adc9-806be4aaab77'),
        'text': 'Choose the word that best completes the analogy: ALGORITHM is to PROGRAMMER as BLUEPRINT is to:',
        'text_urdu': 'مناسب ترین لفظ منتخب کریں: الگورتھم کا جو تعلق پروگرامر سے ہے، وہی تعلق بلیو پرنٹ (نقشہ) کا کس سے ہے؟',
        'type': Question.TypeChoice.MCQ,
        'category': Question.CategoryChoice.APTITUDE,
        'dimension': 'VerbalReasoning',
        'subcategory': 'Analogies',
        'difficulty': Question.DifficultyChoice.BASIC,
        'target_audience': Question.TargetAudienceChoice.MATRIC,
        'order': 12,
        'correct_answer': 'A',
        'correct_answer_weight': 1.0,
        'explanation': 'A programmer creates and executes algorithms; an architect creates and executes blueprints for buildings.',
        'explanation_urdu': 'پروگرامر سافٹ ویئر کے لیے الگورتھم بناتا ہے، جبکہ ماہرِ تعمیرات (آرکیٹیکٹ) عمارت کے لیے بلیو پرنٹ بناتا ہے۔',
        'options': [
            {'id': 'A', 'text': 'ARCHITECT', 'text_urdu': 'ماہرِ تعمیرات (Architect)'},
            {'id': 'B', 'text': 'CARPENTER', 'text_urdu': 'بڑھئی (Carpenter)'},
            {'id': 'C', 'text': 'ELECTRICIAN', 'text_urdu': 'الیکٹریشن'},
            {'id': 'D', 'text': 'DOCTOR', 'text_urdu': 'ڈاکٹر'}
        ]
    },
    {
        'question_id': uuid.UUID('63a49d11-3fcf-4b82-b560-9aff4613854a'),
        'text': 'Which of the following statements is the most logically valid inference from: "All engineers have studied calculus. Some engineers are software developers."',
        'text_urdu': 'اس بیان کا درست منطقی نتیجہ کیا ہے: "تمام انجینئرز نے کیلکولس پڑھا ہے۔ کچھ انجینئرز سافٹ ویئر ڈویلپرز ہیں۔"',
        'type': Question.TypeChoice.MCQ,
        'category': Question.CategoryChoice.APTITUDE,
        'dimension': 'VerbalReasoning',
        'subcategory': 'LogicalDeduction',
        'difficulty': Question.DifficultyChoice.INTERMEDIATE,
        'target_audience': Question.TargetAudienceChoice.MATRIC,
        'order': 13,
        'correct_answer': 'D',
        'correct_answer_weight': 1.0,
        'explanation': 'Since some engineers are software developers, and all engineers studied calculus, those engineers who are developers must have studied calculus.',
        'explanation_urdu': 'چونکہ کچھ انجینئرز سافٹ ویئر ڈویلپرز ہیں اور تمام انجینئرز نے کیلکولس پڑھا ہے، اس لیے وہ ڈویلپرز جو انجینئر ہیں انہوں نے کیلکولس ضرور پڑھا ہے۔',
        'options': [
            {'id': 'A', 'text': 'All software developers have studied calculus.', 'text_urdu': 'تمام سافٹ ویئر ڈویلپرز نے کیلکولس پڑھا ہے۔'},
            {'id': 'B', 'text': 'No software developers study calculus.', 'text_urdu': 'کوئی سافٹ ویئر ڈویلپر کیلکولس نہیں پڑھتا۔'},
            {'id': 'C', 'text': 'Every calculus student is an engineer.', 'text_urdu': 'ہر کیلکولس کا طالب علم انجینئر ہے۔'},
            {'id': 'D', 'text': 'Some software developers have studied calculus.', 'text_urdu': 'کچھ سافٹ ویئر ڈویلپرز نے یقیناً کیلکولس پڑھ رکھا ہے۔'}
        ]
    },
    {
        'question_id': uuid.UUID('7b19a101-1111-4000-8000-000000000006'),
        'text': 'Choose the word that is most nearly OPPOSITE in meaning (antonym) to: "EXPAND".',
        'text_urdu': 'لفظ "EXPAND" (پھیلنا یا وسعت پانا) کا متضاد لفظ منتخب کریں۔',
        'type': Question.TypeChoice.MCQ,
        'category': Question.CategoryChoice.APTITUDE,
        'dimension': 'VerbalReasoning',
        'subcategory': 'Antonyms',
        'difficulty': Question.DifficultyChoice.BASIC,
        'target_audience': Question.TargetAudienceChoice.MATRIC,
        'order': 14,
        'correct_answer': 'C',
        'correct_answer_weight': 1.0,
        'explanation': 'Expand means to increase in size or volume; Contract means to decrease in size.',
        'explanation_urdu': 'Expand کا مطلب ہے پھیلنا، جبکہ اس کا الٹ Contract (سکڑنا یا سمٹنا) ہے۔',
        'options': [
            {'id': 'A', 'text': 'Enlarge', 'text_urdu': 'بڑا کرنا'},
            {'id': 'B', 'text': 'Strengthen', 'text_urdu': 'مضبوط بنانا'},
            {'id': 'C', 'text': 'Contract', 'text_urdu': 'سکڑنا / سمٹنا (Contract)'},
            {'id': 'D', 'text': 'Develop', 'text_urdu': 'ترقی دینا'}
        ]
    },
    {
        'question_id': uuid.UUID('7b19a101-1111-4000-8000-000000000007'),
        'text': 'Read the short statement: "In arid agricultural regions of Sindh, lining irrigation canals with impermeable cement significantly reduces water seepage losses compared to unlined earthen canals, preserving reservoir storage for downstream crops during dry seasons." Based on this statement, what is the primary benefit of lined canals?',
        'text_urdu': 'اس تحریر کو پڑھیں: "سندھ کے خشک زرعی علاقوں میں، نہروں کو سیمنٹ سے پختہ کرنے سے کچی نہروں کے مقابلے میں پانی کا زیرِ زمین رساؤ نمایاں طور پر کم ہو جاتا ہے، جس سے خشک موسم میں فصلوں کے لیے ڈیموں کا پانی محفوظ رہتا ہے۔" اس بیان کی روشنی میں پختہ نہروں کا سب سے بڑا فائدہ کیا ہے؟',
        'type': Question.TypeChoice.MCQ,
        'category': Question.CategoryChoice.APTITUDE,
        'dimension': 'VerbalReasoning',
        'subcategory': 'ReadingComprehension',
        'difficulty': Question.DifficultyChoice.CHALLENGING,
        'target_audience': Question.TargetAudienceChoice.MATRIC,
        'order': 15,
        'correct_answer': 'B',
        'correct_answer_weight': 1.0,
        'explanation': 'The text directly states that lining canals reduces water seepage losses, thereby preserving stored water.',
        'explanation_urdu': 'عبارت کے مطابق سیمنٹ کی پختگی پانی کے رساؤ کے ضیاع کو روکتی ہے جس سے پانی محفوظ رہتا ہے۔',
        'options': [
            {'id': 'A', 'text': 'They accelerate crop maturation speed.', 'text_urdu': 'وہ فصلوں کے پکنے کی رفتار بڑھاتی ہیں۔'},
            {'id': 'B', 'text': 'They prevent water loss through ground seepage.', 'text_urdu': 'وہ زمین میں پانی کے رساؤ کے ذریعے ضیاع کو روکتی ہیں۔'},
            {'id': 'C', 'text': 'They eliminate the need for rainfall entirely.', 'text_urdu': 'وہ بارش کی ضرورت کو بالکل ختم کر دیتی ہیں۔'},
            {'id': 'D', 'text': 'They lower the financial cost of agricultural harvesting.', 'text_urdu': 'وہ فصل کی کٹائی کے اخراجات کم کرتی ہیں۔'}
        ]
    },

    # --- D. SPATIAL VISUALIZATION (5 Items) ---
    {
        'question_id': uuid.UUID('7e0c7e08-6044-4274-91f5-4b38aaa0eb3a'),
        'text': 'Imagine a solid cube with side length 3 cm painted green on all exterior faces. If it is sliced into 1 cm small unit cubes, how many unit cubes will have exactly TWO faces painted green?',
        'text_urdu': 'ایک 3 سینٹی میٹر کا ٹھوس مکعب (Cube) تمام بیرونی اطراف سے سبز رنگا ہوا ہے۔ اگر اسے 1 سینٹی میٹر کے چھوٹے مکعبوں میں کاٹا جائے، تو کتنے چھوٹے مکعبوں کی ٹھیک 2 اطراف سبز ہوں گی؟',
        'type': Question.TypeChoice.MCQ,
        'category': Question.CategoryChoice.APTITUDE,
        'dimension': 'SpatialVisualization',
        'subcategory': '3DCubeAnalysis',
        'difficulty': Question.DifficultyChoice.INTERMEDIATE,
        'target_audience': Question.TargetAudienceChoice.MATRIC,
        'order': 16,
        'correct_answer': 'C',
        'correct_answer_weight': 1.0,
        'explanation': 'A 3x3x3 cube has 12 edges. Each edge has (3 - 2) = 1 middle cube with exactly two painted faces. Total = 12 * 1 = 12 cubes.',
        'explanation_urdu': '3x3x3 مکعب کے 12 کنارے ہوتے ہیں۔ ہر کنارے کے درمیان 1 مکعب ایسا ہوتا ہے جس کی 2 اطراف رنگی ہوتی ہیں۔ کل تعداد = 12 ضرب 1 = 12۔',
        'options': [
            {'id': 'A', 'text': '6 cubes', 'text_urdu': '6 مکعب'},
            {'id': 'B', 'text': '8 cubes', 'text_urdu': '8 مکعب'},
            {'id': 'C', 'text': '12 cubes', 'text_urdu': '12 مکعب'},
            {'id': 'D', 'text': '24 cubes', 'text_urdu': '24 مکعب'}
        ]
    },
    {
        'question_id': uuid.UUID('1bb0e277-63d5-4029-8344-d1232c85e539'),
        'text': 'If a flat square sheet of paper is folded in half precisely along its diagonal from one corner to the opposite corner, what 2D geometric shape is formed?',
        'text_urdu': 'اگر ایک ہموار چوکور (مربع) کاغذ کو اس کے ایک کونے سے مخالف کونے تک ترچھا (Diagonal) بالکل درمیان سے موڑا جائے، تو کون سی دو جہتی شکل بنے گی؟',
        'type': Question.TypeChoice.MCQ,
        'category': Question.CategoryChoice.APTITUDE,
        'dimension': 'SpatialVisualization',
        'subcategory': 'MentalFolding',
        'difficulty': Question.DifficultyChoice.BASIC,
        'target_audience': Question.TargetAudienceChoice.MATRIC,
        'order': 17,
        'correct_answer': 'A',
        'correct_answer_weight': 1.0,
        'explanation': 'Folding a square along its diagonal splits the 90-degree corner and forms a right-angled isosceles triangle.',
        'explanation_urdu': 'مربع کو اس کے وتر کے ساتھ موڑنے سے ایک قائمۃ الزاویہ مثلث (Right-angled Triangle) وجود میں آتی ہے۔',
        'options': [
            {'id': 'A', 'text': 'A right-angled triangle', 'text_urdu': 'قائمۃ الزاویہ مثلث (Right-angled Triangle)'},
            {'id': 'B', 'text': 'A smaller square', 'text_urdu': 'ایک چھوٹا مربع'},
            {'id': 'C', 'text': 'A rectangle', 'text_urdu': 'ایک مستطیل'},
            {'id': 'D', 'text': 'A parallelogram', 'text_urdu': 'متوازی الاضلاع'}
        ]
    },
    {
        'question_id': uuid.UUID('7b19a101-1111-4000-8000-000000000008'),
        'text': 'Which of the following capital English letters possesses BOTH a horizontal line of symmetry and a vertical line of symmetry?',
        'text_urdu': 'درج ذیل انگریزی کے بڑے حروف میں سے کس حرف میں افقی (Horizontal) اور عمودی (Vertical) دونوں طرح کے مماثلت کے خطوط (Lines of Symmetry) موجود ہیں؟',
        'type': Question.TypeChoice.MCQ,
        'category': Question.CategoryChoice.APTITUDE,
        'dimension': 'SpatialVisualization',
        'subcategory': 'Symmetry',
        'difficulty': Question.DifficultyChoice.BASIC,
        'target_audience': Question.TargetAudienceChoice.MATRIC,
        'order': 18,
        'correct_answer': 'C',
        'correct_answer_weight': 1.0,
        'explanation': 'The letter H can be divided symmetrically down the vertical middle and across the horizontal bar. A only has vertical; B only has horizontal; M only has vertical.',
        'explanation_urdu': 'حرف "H" کو درمیان سے عمودی اور افقی دونوں رخ پر دو برابر حصوں میں تقسیم کیا جا سکتا ہے۔',
        'options': [
            {'id': 'A', 'text': 'A', 'text_urdu': 'A'},
            {'id': 'B', 'text': 'B', 'text_urdu': 'B'},
            {'id': 'C', 'text': 'H', 'text_urdu': 'H'},
            {'id': 'D', 'text': 'M', 'text_urdu': 'M'}
        ]
    },
    {
        'question_id': uuid.UUID('7b19a101-1111-4000-8000-000000000009'),
        'text': 'A 2D cardboard pattern (net) consists of one square base in the center with an identical triangle attached to each of its four edges. When folded upward along the edges, which 3D shape does it form?',
        'text_urdu': 'گتے کی ایک دو جہتی ساخت میں درمیان میں ایک مربع بنیاد ہے اور اس کے چاروں کناروں پر چار برابر مثلثیں جڑی ہیں۔ کناروں کے ساتھ اوپر موڑنے پر کون سی 3D شکل بنے گی؟',
        'type': Question.TypeChoice.MCQ,
        'category': Question.CategoryChoice.APTITUDE,
        'dimension': 'SpatialVisualization',
        'subcategory': 'NetFolding',
        'difficulty': Question.DifficultyChoice.INTERMEDIATE,
        'target_audience': Question.TargetAudienceChoice.MATRIC,
        'order': 19,
        'correct_answer': 'B',
        'correct_answer_weight': 1.0,
        'explanation': 'A square base with four triangular sides meeting at a single apex forms a square-based pyramid.',
        'explanation_urdu': 'مربع بنیاد کے اوپر چار مثلثوں کے ملنے سے مربع بنیاد کا اہرام (Square-based Pyramid) بنتا ہے۔',
        'options': [
            {'id': 'A', 'text': 'Cube', 'text_urdu': 'مکعب (Cube)'},
            {'id': 'B', 'text': 'Square-based Pyramid', 'text_urdu': 'مربع بنیاد کا اہرام (Pyramid)'},
            {'id': 'C', 'text': 'Triangular Prism', 'text_urdu': 'مثلثی منشور (Prism)'},
            {'id': 'D', 'text': 'Tetrahedron', 'text_urdu': 'چار سطحی شکل'}
        ]
    },
    {
        'question_id': uuid.UUID('7b19a101-1111-4000-8000-000000000010'),
        'text': 'Looking directly down from above (orthogonal top/bird\'s-eye view) at a cylindrical overhead water tank capped with a conical roof, what 2D geometry would you observe?',
        'text_urdu': 'اگر ایک گول سلنڈر نما پانی کے ٹینک کو جس کی چھت مخروطی (Cone) ہو، بالکل اوپر سے (Bird\'s-eye View) دیکھا جائے، تو کون سی 2D شکل نظر آئے گی؟',
        'type': Question.TypeChoice.MCQ,
        'category': Question.CategoryChoice.APTITUDE,
        'dimension': 'SpatialVisualization',
        'subcategory': 'OrthogonalProjection',
        'difficulty': Question.DifficultyChoice.CHALLENGING,
        'target_audience': Question.TargetAudienceChoice.MATRIC,
        'order': 20,
        'correct_answer': 'A',
        'correct_answer_weight': 1.0,
        'explanation': 'From top view, both cylinder and cone project as a circular outline, with the apex of the cone appearing as a central point.',
        'explanation_urdu': 'اوپر سے دیکھنے پر سلنڈر اور مخروط دونوں گول دائرے کے طور پر نظر آئیں گے جس کے مرکز میں نوک دار نقطہ ہوگا۔',
        'options': [
            {'id': 'A', 'text': 'A circle with a central point', 'text_urdu': 'ایک دائرہ جس کے مرکز میں نقطہ ہو'},
            {'id': 'B', 'text': 'A triangle over a rectangle', 'text_urdu': 'مستطیل کے اوپر مثلث'},
            {'id': 'C', 'text': 'Two concentric squares', 'text_urdu': 'دو باہم ہم مرکز چوکور'},
            {'id': 'D', 'text': 'An ellipse', 'text_urdu': 'بیضوی شکل'}
        ]
    },

    # --- E. SCIENTIFIC REASONING (4 Items) ---
    {
        'question_id': uuid.UUID('baa1b19b-e677-496c-b1ec-18ac571084b4'),
        'text': 'Two identical potted rose plants are provided equal amounts of water and soil nutrients, but Plant A is kept in direct sunlight while Plant B is kept in a dark room. After two weeks, Plant A is healthy and green, whereas Plant B is yellow and wilted. Which variable directly caused this difference?',
        'text_urdu': 'گلاب کے دو یکساں پودوں کو پانی اور کھاد یکساں دی گئی۔ پودا A کھلی دھوپ میں رکھا گیا جبکہ پودا B اندھیرے کمرے میں۔ دو ہفتوں بعد پودا A سرسبز رہا جبکہ پودا B زرد پڑ کر مرجھا گیا۔ اس فرق کی بنیادی وجہ کون سا متغیر ہے؟',
        'type': Question.TypeChoice.MCQ,
        'category': Question.CategoryChoice.APTITUDE,
        'dimension': 'ScientificReasoning',
        'subcategory': 'ExperimentalVariables',
        'difficulty': Question.DifficultyChoice.BASIC,
        'target_audience': Question.TargetAudienceChoice.MATRIC,
        'order': 21,
        'correct_answer': 'A',
        'correct_answer_weight': 1.0,
        'explanation': 'Sunlight availability was the single manipulated independent variable necessary for photosynthesis and chlorophyll production.',
        'explanation_urdu': 'دھوپ کی دستیابی وہ واحد آزاد متغیر تھا جو ضیائی تالیف (Photosynthesis) اور سبز مادے کی تشکیل کے لیے درکار تھا۔',
        'options': [
            {'id': 'A', 'text': 'Sunlight availability for photosynthesis', 'text_urdu': 'روشنی کی دستیابی (Photosynthesis کے لیے)'},
            {'id': 'B', 'text': 'The color of the pot', 'text_urdu': 'گملے کا رنگ'},
            {'id': 'C', 'text': 'The mineral composition of the soil', 'text_urdu': 'مٹی کی ساخت'},
            {'id': 'D', 'text': 'The temperature of the tap water', 'text_urdu': 'پانی کا درجہ حرارت'}
        ]
    },
    {
        'question_id': uuid.UUID('7b19a101-1111-4000-8000-000000000011'),
        'text': 'A solid steel needle sinks immediately when placed in a bowl of water, but a heavy wooden block weighing 10 kilograms floats easily. What is the fundamental physical principle explaining this?',
        'text_urdu': 'لوہے کی ایک چھوٹی سوئی پانی کے پیالے میں فوراً ڈوب جاتی ہے، جبکہ 10 کلو وزنی لکڑی کا بڑا ٹکڑا پانی پر باآسانی تیرتا ہے۔ اس کی بنیادی سائنسی وجہ کیا ہے؟',
        'type': Question.TypeChoice.MCQ,
        'category': Question.CategoryChoice.APTITUDE,
        'dimension': 'ScientificReasoning',
        'subcategory': 'DensityAndBuoyancy',
        'difficulty': Question.DifficultyChoice.BASIC,
        'target_audience': Question.TargetAudienceChoice.MATRIC,
        'order': 22,
        'correct_answer': 'B',
        'correct_answer_weight': 1.0,
        'explanation': 'Flotation depends on density, not total mass. Steel has a higher density than water, while wood has a lower density than water.',
        'explanation_urdu': 'تیرنے کا انحصار کثافت (Density) پر ہوتا ہے کل وزن پر نہیں۔ فولاد کی کثافت پانی سے زیادہ ہے جبکہ لکڑی کی کثافت پانی سے کم ہے۔',
        'options': [
            {'id': 'A', 'text': 'Wood has greater magnetic properties than steel.', 'text_urdu': 'لکڑی میں فولاد سے زیادہ مقناطیسی اثر ہوتا ہے۔'},
            {'id': 'B', 'text': 'Steel has higher density than water, while wood has lower density than water.', 'text_urdu': 'فولاد کی کثافت پانی سے زیادہ ہے جبکہ لکڑی کی کثافت پانی سے کم ہے۔'},
            {'id': 'C', 'text': 'The needle has more total gravitational mass than the wooden block.', 'text_urdu': 'سوئی کی کشش ثقل لکڑی سے زیادہ ہے۔'},
            {'id': 'D', 'text': 'Surface tension exclusively repels wooden objects.', 'text_urdu': 'پانی کی سطحی کشش صرف لکڑی کو اوپر رکھتی ہے۔'}
        ]
    },
    {
        'question_id': uuid.UUID('7b19a101-1111-4000-8000-000000000012'),
        'text': 'When pure ice cubes at 0°C are heated slowly, they turn into liquid water at 0°C without any rise in temperature until all ice has melted. What is happening to the heat energy supplied during this transition?',
        'text_urdu': 'جب 0 ڈگری سینٹی گریڈ پر برف کو گرم کیا جائے تو وہ پگھل کر 0 ڈگری پر پانی بنتی ہے اور درجہ حرارت اس وقت تک نہیں بڑھتا جب تک تمام برف پگھل نہ جائے۔ اس دوران دی جانے والی حرارت کہاں استعمال ہوتی ہے؟',
        'type': Question.TypeChoice.MCQ,
        'category': Question.CategoryChoice.APTITUDE,
        'dimension': 'ScientificReasoning',
        'subcategory': 'StatesOfMatter',
        'difficulty': Question.DifficultyChoice.INTERMEDIATE,
        'target_audience': Question.TargetAudienceChoice.MATRIC,
        'order': 23,
        'correct_answer': 'C',
        'correct_answer_weight': 1.0,
        'explanation': 'Heat is absorbed as latent heat of fusion to break intermolecular hydrogen bonds in the crystal lattice without increasing kinetic energy.',
        'explanation_urdu': 'حرارت برف کے مالیکیولز کے درمیان بانڈز توڑنے میں مخفی حرارت (Latent Heat of Fusion) کے طور پر جذب ہوتی ہے۔',
        'options': [
            {'id': 'A', 'text': 'It is destroyed completely according to entropy rules.', 'text_urdu': 'حرارت بالکل ضائع ہو جاتی ہے۔'},
            {'id': 'B', 'text': 'It increases the speed of electrons inside hydrogen atoms.', 'text_urdu': 'یہ ایٹموں کے الیکٹران کی رفتار تیز کرتی ہے۔'},
            {'id': 'C', 'text': 'It is absorbed as latent heat of fusion to break intermolecular bonds.', 'text_urdu': 'یہ مالیکیولز کے درمیانی بندھن توڑنے کے لیے مخفی حرارت کے طور پر استعمال ہوتی ہے۔'},
            {'id': 'D', 'text': 'It radiates out into the air instantaneously.', 'text_urdu': 'یہ فوری طور پر ہوا میں خارج ہو جاتی ہے۔'}
        ]
    },
    {
        'question_id': uuid.UUID('7b19a101-1111-4000-8000-000000000013'),
        'text': 'An agricultural scientist tests whether a new organic fertilizer increases the yield of Sindhri mango trees. To ensure the scientific validity of the experiment, what must be kept strictly controlled across both the experimental and control groups?',
        'text_urdu': 'ایک زرعی سائنسدان یہ تجربہ کرتا ہے کہ کیا نئی کھاد سے سندھڑی آم کے درختوں کی پیداوار بڑھتی ہے۔ سائنسی تحقیق کی درستگی کے لیے کن عوامل کو دونوں گروپوں میں یکساں رکھنا لازمی ہے؟',
        'type': Question.TypeChoice.MCQ,
        'category': Question.CategoryChoice.APTITUDE,
        'dimension': 'ScientificReasoning',
        'subcategory': 'ScientificMethodControls',
        'difficulty': Question.DifficultyChoice.CHALLENGING,
        'target_audience': Question.TargetAudienceChoice.MATRIC,
        'order': 24,
        'correct_answer': 'D',
        'correct_answer_weight': 1.0,
        'explanation': 'In scientific testing, all environmental conditions (soil, water, tree age, sunlight) must remain identical so that fertilizer is the only causal factor.',
        'explanation_urdu': 'تمام بیرونی عوامل (پانی، مٹی، درختوں کی عمر اور دھوپ) کو یکساں رکھنا ضروری ہے تاکہ نتیجہ صرف کھاد کا اثر ثابت کرے۔',
        'options': [
            {'id': 'A', 'text': 'Only the brand of chemical pesticide applied', 'text_urdu': 'صرف کیڑے مار دوا کا برانڈ'},
            {'id': 'B', 'text': 'The market selling price of the harvested fruit', 'text_urdu': 'منڈی میں پھل کی فروخت کی قیمت'},
            {'id': 'C', 'text': 'The amount of fertilizer added to each tree', 'text_urdu': 'کھاد کی مقدار'},
            {'id': 'D', 'text': 'Soil type, water volume, sunlight exposure, and tree age', 'text_urdu': 'مٹی کی قسم، پانی کی مقدار، دھوپ اور درختوں کی عمر'}
        ]
    },

    # --- F. PRACTICAL PROBLEM SOLVING (4 Items) ---
    {
        'question_id': uuid.UUID('77e4f513-b24b-4f0a-9a5f-671621385cf3'),
        'text': 'A student has exactly 2 hours remaining before a major examination and must review three subjects with different exam weights: Mathematics (50% of total marks), Physics (30%), and English (20%). How should the student logically allocate study time?',
        'text_urdu': 'امتحان سے قبل ایک طالب علم کے پاس ٹھیک 2 گھنٹے ہیں اور اسے تین مختلف مضامین دہرانے ہیں جن کے نمبروں کا تناسب یہ ہے: ریاضی (50 فیصد)، فزکس (30 فیصد)، اور انگریزی (20 فیصد)۔ طالب علم کو وقت کی تقسیم کس طرح کرنی چاہیے؟',
        'type': Question.TypeChoice.MCQ,
        'category': Question.CategoryChoice.APTITUDE,
        'dimension': 'PracticalProblemSolving',
        'subcategory': 'ResourceOptimization',
        'difficulty': Question.DifficultyChoice.BASIC,
        'target_audience': Question.TargetAudienceChoice.MATRIC,
        'order': 25,
        'correct_answer': 'B',
        'correct_answer_weight': 1.0,
        'explanation': 'Total time = 120 minutes. Math (50% = 60 mins), Physics (30% = 36 mins), English (20% = 24 mins). This maximizes expected return on marks.',
        'explanation_urdu': 'کل وقت 120 منٹ ہے۔ ریاضی کو 60 منٹ، فزکس کو 36 منٹ اور انگریزی کو 24 منٹ دینے سے زیادہ نمبر حاصل کرنے کے امکانات بڑھتے ہیں۔',
        'options': [
            {'id': 'A', 'text': 'Spend 40 minutes equally on each subject regardless of marks.', 'text_urdu': 'نمبروں کو نظر انداز کر کے ہر مضمون کو برابر 40 منٹ دیں۔'},
            {'id': 'B', 'text': 'Allocate 60 mins to Math, 36 mins to Physics, and 24 mins to English in proportion to exam weights.', 'text_urdu': 'نمبروں کے تناسب سے ریاضی کو 60 منٹ، فزکس کو 36 منٹ اور انگریزی کو 24 منٹ دیں۔'},
            {'id': 'C', 'text': 'Spend the entire 2 hours only on the easiest subject.', 'text_urdu': 'مکمل دو گھنٹے صرف سب سے آسان مضمون پر صرف کریں۔'},
            {'id': 'D', 'text': 'Skip all review and start the test without revision.', 'text_urdu': 'بغیر دہرائے سیدھا امتحان دینے چلے جائیں۔'}
        ]
    },
    {
        'question_id': uuid.UUID('7b19a101-1111-4000-8000-000000000014'),
        'text': 'A school science club has a fixed budget of 5,000 PKR to equip their chemistry bench. Glass beakers cost 500 PKR each and test tube packs cost 250 PKR each. If they require at least 4 beakers, what is the maximum number of test tube packs they can purchase with the remaining funds?',
        'text_urdu': 'سائنس کلب کے پاس سامان کے لیے 5,000 روپے کا بجٹ ہے۔ ایک بیکر کی قیمت 500 روپے اور ٹیسٹ ٹیوب پیک کی قیمت 250 روپے ہے۔ اگر کم از کم 4 بیکر لینا لازمی ہوں، تو باقی رقم سے زیادہ سے زیادہ کتنے ٹیسٹ ٹیوب پیک خریدے جا سکتے ہیں؟',
        'type': Question.TypeChoice.MCQ,
        'category': Question.CategoryChoice.APTITUDE,
        'dimension': 'PracticalProblemSolving',
        'subcategory': 'BudgetOptimization',
        'difficulty': Question.DifficultyChoice.INTERMEDIATE,
        'target_audience': Question.TargetAudienceChoice.MATRIC,
        'order': 26,
        'correct_answer': 'C',
        'correct_answer_weight': 1.0,
        'explanation': 'Cost of 4 beakers = 4 * 500 = 2,000 PKR. Remaining funds = 5,000 - 2,000 = 3,000 PKR. Test tube packs = 3,000 / 250 = 12 packs.',
        'explanation_urdu': '4 بیکروں کی قیمت = 4 ضرب 500 = 2,000 روپے۔ باقی بجٹ = 3,000 روپے۔ ٹیسٹ ٹیوب پیک = 3,000 تقسیم 250 = 12 پیک۔',
        'options': [
            {'id': 'A', 'text': '8 packs', 'text_urdu': '8 پیک'},
            {'id': 'B', 'text': '10 packs', 'text_urdu': '10 پیک'},
            {'id': 'C', 'text': '12 packs', 'text_urdu': '12 پیک'},
            {'id': 'D', 'text': '14 packs', 'text_urdu': '14 پیک'}
        ]
    },
    {
        'question_id': uuid.UUID('7b19a101-1111-4000-8000-000000000015'),
        'text': 'A team must deliver an engineering exhibition project by Friday morning. The workflow consists of four sequential stages that cannot overlap: Schematic Design (1 day), Component Sourcing (2 days), Hardware Assembly (1 day), and Final Testing (1 day). By which day must Schematic Design begin?',
        'text_urdu': 'ایک ٹیم نے جمعہ کی صبح انجینئرنگ نمائش کا پراجیکٹ جمع کروانا ہے۔ اس کے چار لازمی مراحل ہیں جو باری باری ہی ہو سکتے ہیں: خاکہ ڈیزائننگ (1 دن)، پرزہ جات کی خریداری (2 دن)، اسمبلنگ (1 دن)، اور حتمی ٹیسٹنگ (1 دن)۔ ڈیزائننگ کا کام کس دن شروع ہونا لازمی ہے؟',
        'type': Question.TypeChoice.MCQ,
        'category': Question.CategoryChoice.APTITUDE,
        'dimension': 'PracticalProblemSolving',
        'subcategory': 'ProjectScheduling',
        'difficulty': Question.DifficultyChoice.CHALLENGING,
        'target_audience': Question.TargetAudienceChoice.MATRIC,
        'order': 27,
        'correct_answer': 'A',
        'correct_answer_weight': 1.0,
        'explanation': 'Total days required = 1 + 2 + 1 + 1 = 5 working days. Working backwards from Friday: Thursday (Testing), Wednesday (Assembly), Tuesday & Monday (Sourcing), Monday morning (Design).',
        'explanation_urdu': 'کل درکار وقت = 1 + 2 + 1 + 1 = 5 دن۔ جمعہ سے الٹی گنتی کریں: جمعرات (ٹیسٹنگ)، بدھ (اسمبلنگ)، منگل و پیر (خریداری)، لہٰذا پیر کی صبح کام شروع ہونا ضروری ہے۔',
        'options': [
            {'id': 'A', 'text': 'Monday morning', 'text_urdu': 'پیر کی صبح'},
            {'id': 'B', 'text': 'Tuesday morning', 'text_urdu': 'منگل کی صبح'},
            {'id': 'C', 'text': 'Wednesday morning', 'text_urdu': 'بدھ کی صبح'},
            {'id': 'D', 'text': 'Previous Saturday', 'text_urdu': 'پچھلا ہفتہ'}
        ]
    },
    {
        'question_id': uuid.UUID('7b19a101-1111-4000-8000-000000000016'),
        'text': 'A student turns on a desktop computer in the school computer lab, but the monitor screen remains completely black and no power indicator lights illuminate. What is the most logical and efficient first troubleshooting step?',
        'text_urdu': 'طالب علم کمپیوٹر لیب میں کمپیوٹر آن کرتا ہے مگر مانیٹر کی اسکرین بالکل کالی رہتی ہے اور کوئی لائٹ نہیں جلتی۔ مسئلے کی نشاندہی کے لیے سب سے پہلا اور منطقی قدم کیا ہونا چاہیے؟',
        'type': Question.TypeChoice.MCQ,
        'category': Question.CategoryChoice.APTITUDE,
        'dimension': 'PracticalProblemSolving',
        'subcategory': 'SystemTroubleshooting',
        'difficulty': Question.DifficultyChoice.BASIC,
        'target_audience': Question.TargetAudienceChoice.MATRIC,
        'order': 28,
        'correct_answer': 'C',
        'correct_answer_weight': 1.0,
        'explanation': 'Basic troubleshooting starts with verifying physical electrical connectivity before assuming hardware or software failure.',
        'explanation_urdu': 'بنیادی تکنیکی اصول کے مطابق سب سے پہلے پاور کیبل اور ساکٹ کی بجلی چیک کرنی چاہیے۔',
        'options': [
            {'id': 'A', 'text': 'Reinstall the operating system software immediately.', 'text_urdu': 'آپریٹنگ سسٹم کو فوری طور پر دوبارہ انسٹال کریں۔'},
            {'id': 'B', 'text': 'Open the computer chassis and replace the central processor.', 'text_urdu': 'کمپیوٹر کھول کر پروسیسر تبدیل کر دیں۔'},
            {'id': 'C', 'text': 'Check if the main power cable is securely plugged in and the wall socket is turned on.', 'text_urdu': 'چیک کریں کہ پاور کیبل ساکٹ میں لگی ہے اور بجلی کا بٹن آن ہے۔'},
            {'id': 'D', 'text': 'Purchase a brand new display monitor.', 'text_urdu': 'نیا مانیٹر خرید لیں۔'}
        ]
    },

    # ==========================================================================
    # SECTION 2: RIASEC CAREER INTEREST INVENTORY (24 ITEMS, 4 PER DIMENSION)
    # Balanced 1 to 5 Likert Scale: Strongly Disagree to Strongly Agree
    # ==========================================================================

    # --- REALISTIC (4 Items) ---
    {
        'question_id': uuid.UUID('3c457547-a67a-4f6d-b102-dbc91571a02c'),
        'text': 'I prefer hands-on activities, working with machinery, assembling physical mechanisms, electronic circuits, or building hardware.',
        'text_urdu': 'مجھے عملی کام کرنا، مشینوں کے ساتھ کام کرنا، آلات بنانا اور الیکٹرانک آلات کی مرمت کرنا پسند ہے۔',
        'type': Question.TypeChoice.LIKERT,
        'category': Question.CategoryChoice.INTEREST,
        'dimension': 'RIASEC_Realistic',
        'target_audience': Question.TargetAudienceChoice.MATRIC,
        'order': 29,
        'options': [
            {'id': '1', 'text': 'Strongly Disagree', 'text_urdu': 'بالکل متفق نہیں', 'score': 1.0},
            {'id': '2', 'text': 'Disagree', 'text_urdu': 'متفق نہیں', 'score': 2.0},
            {'id': '3', 'text': 'Neutral', 'text_urdu': 'غیر جانبدار', 'score': 3.0},
            {'id': '4', 'text': 'Agree', 'text_urdu': 'متفق ہوں', 'score': 4.0},
            {'id': '5', 'text': 'Strongly Agree', 'text_urdu': 'مکمل متفق ہوں', 'score': 5.0}
        ]
    },
    {
        'question_id': uuid.UUID('6c0c52ae-754a-4986-a8e8-a5aa47f1a22e'),
        'text': 'I enjoy repairing household devices, servicing mechanical parts, or learning how vehicle engines and motors work.',
        'text_urdu': 'مجھے گھریلو برقی اشیاء ٹھیک کرنا، پرزے جوڑنا یا یہ سیکھنا اچھا لگتا ہے کہ انجن اور موٹریں کیسے کام کرتی ہیں۔',
        'type': Question.TypeChoice.LIKERT,
        'category': Question.CategoryChoice.INTEREST,
        'dimension': 'RIASEC_Realistic',
        'target_audience': Question.TargetAudienceChoice.MATRIC,
        'order': 30,
        'options': [
            {'id': '1', 'text': 'Strongly Disagree', 'text_urdu': 'بالکل متفق نہیں', 'score': 1.0},
            {'id': '2', 'text': 'Disagree', 'text_urdu': 'متفق نہیں', 'score': 2.0},
            {'id': '3', 'text': 'Neutral', 'text_urdu': 'غیر جانبدار', 'score': 3.0},
            {'id': '4', 'text': 'Agree', 'text_urdu': 'متفق ہوں', 'score': 4.0},
            {'id': '5', 'text': 'Strongly Agree', 'text_urdu': 'مکمل متفق ہوں', 'score': 5.0}
        ]
    },
    {
        'question_id': uuid.UUID('7b19a102-2222-4000-8000-000000000001'),
        'text': 'I like working outdoors with construction tools, technical survey equipment, or agricultural machinery.',
        'text_urdu': 'مجھے کھلے میدان میں تعمیری اوزاروں، پیمائشی آلات یا زرعی مشینوں کے ساتھ کام کرنا اچھا لگتا ہے۔',
        'type': Question.TypeChoice.LIKERT,
        'category': Question.CategoryChoice.INTEREST,
        'dimension': 'RIASEC_Realistic',
        'target_audience': Question.TargetAudienceChoice.MATRIC,
        'order': 31,
        'options': [
            {'id': '1', 'text': 'Strongly Disagree', 'text_urdu': 'بالکل متفق نہیں', 'score': 1.0},
            {'id': '2', 'text': 'Disagree', 'text_urdu': 'متفق نہیں', 'score': 2.0},
            {'id': '3', 'text': 'Neutral', 'text_urdu': 'غیر جانبدار', 'score': 3.0},
            {'id': '4', 'text': 'Agree', 'text_urdu': 'متفق ہوں', 'score': 4.0},
            {'id': '5', 'text': 'Strongly Agree', 'text_urdu': 'مکمل متفق ہوں', 'score': 5.0}
        ]
    },
    {
        'question_id': uuid.UUID('7b19a102-2222-4000-8000-000000000002'),
        'text': 'I find deep satisfaction in crafting tangible objects from wood, metal, or plastic following precise technical drawings.',
        'text_urdu': 'مجھے تکنیکی خاکوں کی مدد سے لکڑی، دھات یا پلاسٹک سے ٹھوس اشیاء تیار کرنے میں خوشی محسوس ہوتی ہے۔',
        'type': Question.TypeChoice.LIKERT,
        'category': Question.CategoryChoice.INTEREST,
        'dimension': 'RIASEC_Realistic',
        'target_audience': Question.TargetAudienceChoice.MATRIC,
        'order': 32,
        'options': [
            {'id': '1', 'text': 'Strongly Disagree', 'text_urdu': 'بالکل متفق نہیں', 'score': 1.0},
            {'id': '2', 'text': 'Disagree', 'text_urdu': 'متفق نہیں', 'score': 2.0},
            {'id': '3', 'text': 'Neutral', 'text_urdu': 'غیر جانبدار', 'score': 3.0},
            {'id': '4', 'text': 'Agree', 'text_urdu': 'متفق ہوں', 'score': 4.0},
            {'id': '5', 'text': 'Strongly Agree', 'text_urdu': 'مکمل متفق ہوں', 'score': 5.0}
        ]
    },

    # --- INVESTIGATIVE (4 Items) ---
    {
        'question_id': uuid.UUID('4b19aff1-3aee-4037-ab72-76a57a79939b'),
        'text': 'I enjoy analyzing scientific phenomena, solving challenging mathematical puzzles, and understanding how natural laws operate.',
        'text_urdu': 'مجھے سائنسی حقائق کا جائزہ لینا، ریاضیاتی گتھیاں سلجھانا اور کائنات کے قوانین کو سمجھنا اچھا لگتا ہے۔',
        'type': Question.TypeChoice.LIKERT,
        'category': Question.CategoryChoice.INTEREST,
        'dimension': 'RIASEC_Investigative',
        'target_audience': Question.TargetAudienceChoice.MATRIC,
        'order': 33,
        'options': [
            {'id': '1', 'text': 'Strongly Disagree', 'text_urdu': 'بالکل متفق نہیں', 'score': 1.0},
            {'id': '2', 'text': 'Disagree', 'text_urdu': 'متفق نہیں', 'score': 2.0},
            {'id': '3', 'text': 'Neutral', 'text_urdu': 'غیر جانبدار', 'score': 3.0},
            {'id': '4', 'text': 'Agree', 'text_urdu': 'متفق ہوں', 'score': 4.0},
            {'id': '5', 'text': 'Strongly Agree', 'text_urdu': 'مکمل متفق ہوں', 'score': 5.0}
        ]
    },
    {
        'question_id': uuid.UUID('3ed32e66-c342-4daa-826d-e09374e3d46f'),
        'text': 'I like conducting experiments in a science laboratory, observing microscopic specimens, and discovering why chemical reactions happen.',
        'text_urdu': 'مجھے سائنس لیب میں تجربات کرنا، خوردبین کے ذریعے نمونے دیکھنا اور کیمیائی ردِ عمل کی وجوہات جاننا پسند ہے۔',
        'type': Question.TypeChoice.LIKERT,
        'category': Question.CategoryChoice.INTEREST,
        'dimension': 'RIASEC_Investigative',
        'target_audience': Question.TargetAudienceChoice.MATRIC,
        'order': 34,
        'options': [
            {'id': '1', 'text': 'Strongly Disagree', 'text_urdu': 'بالکل متفق نہیں', 'score': 1.0},
            {'id': '2', 'text': 'Disagree', 'text_urdu': 'متفق نہیں', 'score': 2.0},
            {'id': '3', 'text': 'Neutral', 'text_urdu': 'غیر جانبدار', 'score': 3.0},
            {'id': '4', 'text': 'Agree', 'text_urdu': 'متفق ہوں', 'score': 4.0},
            {'id': '5', 'text': 'Strongly Agree', 'text_urdu': 'مکمل متفق ہوں', 'score': 5.0}
        ]
    },
    {
        'question_id': uuid.UUID('7b19a102-2222-4000-8000-000000000003'),
        'text': 'I enjoy reading science articles or watching educational documentaries explaining genetics, astrophysics, or renewable energy technologies.',
        'text_urdu': 'مجھے سائنسی مضامین پڑھنا یا جینیات، فلکیات اور توانائی کے موضوعات پر معلوماتی ویڈیوز دیکھنا پسند ہے۔',
        'type': Question.TypeChoice.LIKERT,
        'category': Question.CategoryChoice.INTEREST,
        'dimension': 'RIASEC_Investigative',
        'target_audience': Question.TargetAudienceChoice.MATRIC,
        'order': 35,
        'options': [
            {'id': '1', 'text': 'Strongly Disagree', 'text_urdu': 'بالکل متفق نہیں', 'score': 1.0},
            {'id': '2', 'text': 'Disagree', 'text_urdu': 'متفق نہیں', 'score': 2.0},
            {'id': '3', 'text': 'Neutral', 'text_urdu': 'غیر جانبدار', 'score': 3.0},
            {'id': '4', 'text': 'Agree', 'text_urdu': 'متفق ہوں', 'score': 4.0},
            {'id': '5', 'text': 'Strongly Agree', 'text_urdu': 'مکمل متفق ہوں', 'score': 5.0}
        ]
    },
    {
        'question_id': uuid.UUID('7b19a102-2222-4000-8000-000000000004'),
        'text': 'I like identifying the root cause of an error when a computer code fails or a formula produces an unexpected output.',
        'text_urdu': 'جب کوئی کمپیوٹر پروگرام یا حسابی فارمولا غلط نتیجہ دے، تو مجھے اس کی اصل خامی (Bug) تلاش کر کے حل کرنا پسند ہے۔',
        'type': Question.TypeChoice.LIKERT,
        'category': Question.CategoryChoice.INTEREST,
        'dimension': 'RIASEC_Investigative',
        'target_audience': Question.TargetAudienceChoice.MATRIC,
        'order': 36,
        'options': [
            {'id': '1', 'text': 'Strongly Disagree', 'text_urdu': 'بالکل متفق نہیں', 'score': 1.0},
            {'id': '2', 'text': 'Disagree', 'text_urdu': 'متفق نہیں', 'score': 2.0},
            {'id': '3', 'text': 'Neutral', 'text_urdu': 'غیر جانبدار', 'score': 3.0},
            {'id': '4', 'text': 'Agree', 'text_urdu': 'متفق ہوں', 'score': 4.0},
            {'id': '5', 'text': 'Strongly Agree', 'text_urdu': 'مکمل متفق ہوں', 'score': 5.0}
        ]
    },

    # --- ARTISTIC (4 Items) ---
    {
        'question_id': uuid.UUID('78441322-bf3e-42e7-8772-aaab42546248'),
        'text': 'I enjoy creative self-expression through digital graphic design, creative writing, photography, or multimedia storytelling.',
        'text_urdu': 'مجھے بصری ڈیزائننگ، تخلیقی تحریر، آرٹ اور خوبصورت عمارتی ڈیزائن تخلیق کرنے میں لطف آتا ہے۔',
        'type': Question.TypeChoice.LIKERT,
        'category': Question.CategoryChoice.INTEREST,
        'dimension': 'RIASEC_Artistic',
        'target_audience': Question.TargetAudienceChoice.MATRIC,
        'order': 37,
        'options': [
            {'id': '1', 'text': 'Strongly Disagree', 'text_urdu': 'بالکل متفق نہیں', 'score': 1.0},
            {'id': '2', 'text': 'Disagree', 'text_urdu': 'متفق نہیں', 'score': 2.0},
            {'id': '3', 'text': 'Neutral', 'text_urdu': 'غیر جانبدار', 'score': 3.0},
            {'id': '4', 'text': 'Agree', 'text_urdu': 'متفق ہوں', 'score': 4.0},
            {'id': '5', 'text': 'Strongly Agree', 'text_urdu': 'مکمل متفق ہوں', 'score': 5.0}
        ]
    },
    {
        'question_id': uuid.UUID('f67e6aed-a311-4de9-b33a-92b3b6e9e0cc'),
        'text': 'I like freehand sketching, drawing portraits or landscapes, and experimenting with painting techniques and color theory.',
        'text_urdu': 'مجھے ہاتھ سے خاکے بنانا، تصاویر کشی کرنا اور رنگوں کے امتزاج سے نئی پینٹنگز بنانا پسند ہے۔',
        'type': Question.TypeChoice.LIKERT,
        'category': Question.CategoryChoice.INTEREST,
        'dimension': 'RIASEC_Artistic',
        'target_audience': Question.TargetAudienceChoice.MATRIC,
        'order': 38,
        'options': [
            {'id': '1', 'text': 'Strongly Disagree', 'text_urdu': 'بالکل متفق نہیں', 'score': 1.0},
            {'id': '2', 'text': 'Disagree', 'text_urdu': 'متفق نہیں', 'score': 2.0},
            {'id': '3', 'text': 'Neutral', 'text_urdu': 'غیر جانبدار', 'score': 3.0},
            {'id': '4', 'text': 'Agree', 'text_urdu': 'متفق ہوں', 'score': 4.0},
            {'id': '5', 'text': 'Strongly Agree', 'text_urdu': 'مکمل متفق ہوں', 'score': 5.0}
        ]
    },
    {
        'question_id': uuid.UUID('7b19a102-2222-4000-8000-000000000005'),
        'text': 'I enjoy writing short stories, poetry, personal essays, or school drama scripts expressing unique perspectives.',
        'text_urdu': 'مجھے کہانیاں، شاعری، ادبی مضامین لکھنا یا اسکول کے ڈرامے کے ڈائیلاگ تحریر کرنا اچھا لگتا ہے۔',
        'type': Question.TypeChoice.LIKERT,
        'category': Question.CategoryChoice.INTEREST,
        'dimension': 'RIASEC_Artistic',
        'target_audience': Question.TargetAudienceChoice.MATRIC,
        'order': 39,
        'options': [
            {'id': '1', 'text': 'Strongly Disagree', 'text_urdu': 'بالکل متفق نہیں', 'score': 1.0},
            {'id': '2', 'text': 'Disagree', 'text_urdu': 'متفق نہیں', 'score': 2.0},
            {'id': '3', 'text': 'Neutral', 'text_urdu': 'غیر جانبدار', 'score': 3.0},
            {'id': '4', 'text': 'Agree', 'text_urdu': 'متفق ہوں', 'score': 4.0},
            {'id': '5', 'text': 'Strongly Agree', 'text_urdu': 'مکمل متفق ہوں', 'score': 5.0}
        ]
    },
    {
        'question_id': uuid.UUID('7b19a102-2222-4000-8000-000000000006'),
        'text': 'I pay close attention to building facades, interior room decorations, and architectural spatial aesthetics.',
        'text_urdu': 'مجھے عمارتوں کے بیرونی انداز، کمروں کی اندرونی سجاوٹ اور عمارتی خوبصورتی میں گہری دلچسپی ہے۔',
        'type': Question.TypeChoice.LIKERT,
        'category': Question.CategoryChoice.INTEREST,
        'dimension': 'RIASEC_Artistic',
        'target_audience': Question.TargetAudienceChoice.MATRIC,
        'order': 40,
        'options': [
            {'id': '1', 'text': 'Strongly Disagree', 'text_urdu': 'بالکل متفق نہیں', 'score': 1.0},
            {'id': '2', 'text': 'Disagree', 'text_urdu': 'متفق نہیں', 'score': 2.0},
            {'id': '3', 'text': 'Neutral', 'text_urdu': 'غیر جانبدار', 'score': 3.0},
            {'id': '4', 'text': 'Agree', 'text_urdu': 'متفق ہوں', 'score': 4.0},
            {'id': '5', 'text': 'Strongly Agree', 'text_urdu': 'مکمل متفق ہوں', 'score': 5.0}
        ]
    },

    # --- SOCIAL (4 Items) ---
    {
        'question_id': uuid.UUID('5e6c11b2-a2ea-4305-acb2-224c911eeee8'),
        'text': 'I find purpose in counseling individuals, teaching students, caring for patients, and empowering community welfare.',
        'text_urdu': 'مجھے لوگوں کی رہنمائی کرنا، مریضوں کی دیکھ بھال کرنا اور سماجی فلاح کے کاموں میں حصہ لینا پسند ہے۔',
        'type': Question.TypeChoice.LIKERT,
        'category': Question.CategoryChoice.INTEREST,
        'dimension': 'RIASEC_Social',
        'target_audience': Question.TargetAudienceChoice.MATRIC,
        'order': 41,
        'options': [
            {'id': '1', 'text': 'Strongly Disagree', 'text_urdu': 'بالکل متفق نہیں', 'score': 1.0},
            {'id': '2', 'text': 'Disagree', 'text_urdu': 'متفق نہیں', 'score': 2.0},
            {'id': '3', 'text': 'Neutral', 'text_urdu': 'غیر جانبدار', 'score': 3.0},
            {'id': '4', 'text': 'Agree', 'text_urdu': 'متفق ہوں', 'score': 4.0},
            {'id': '5', 'text': 'Strongly Agree', 'text_urdu': 'مکمل متفق ہوں', 'score': 5.0}
        ]
    },
    {
        'question_id': uuid.UUID('e3bea9e7-6eed-4431-8ca4-904089791097'),
        'text': 'I enjoy patiently explaining difficult lessons and study topics to classmates who are struggling with course material.',
        'text_urdu': 'مجھے اپنے ساتھی طلباء کو پڑھائی کے مشکل اسباق اور تصورات تسلی کے ساتھ سمجھانا اچھا لگتا ہے۔',
        'type': Question.TypeChoice.LIKERT,
        'category': Question.CategoryChoice.INTEREST,
        'dimension': 'RIASEC_Social',
        'target_audience': Question.TargetAudienceChoice.MATRIC,
        'order': 42,
        'options': [
            {'id': '1', 'text': 'Strongly Disagree', 'text_urdu': 'بالکل متفق نہیں', 'score': 1.0},
            {'id': '2', 'text': 'Disagree', 'text_urdu': 'متفق نہیں', 'score': 2.0},
            {'id': '3', 'text': 'Neutral', 'text_urdu': 'غیر جانبدار', 'score': 3.0},
            {'id': '4', 'text': 'Agree', 'text_urdu': 'متفق ہوں', 'score': 4.0},
            {'id': '5', 'text': 'Strongly Agree', 'text_urdu': 'مکمل متفق ہوں', 'score': 5.0}
        ]
    },
    {
        'question_id': uuid.UUID('7b19a102-2222-4000-8000-000000000007'),
        'text': 'I am motivated to volunteer in healthcare relief camps, blood donation drives, or literacy programs for underprivileged children.',
        'text_urdu': 'مجھے طبی کیمپوں، خون کے عطیات کی مہم یا پسماندہ بچوں کو مفت پڑھانے کی سماجی سرگرمیوں میں حصہ لینا پسند ہے۔',
        'type': Question.TypeChoice.LIKERT,
        'category': Question.CategoryChoice.INTEREST,
        'dimension': 'RIASEC_Social',
        'target_audience': Question.TargetAudienceChoice.MATRIC,
        'order': 43,
        'options': [
            {'id': '1', 'text': 'Strongly Disagree', 'text_urdu': 'بالکل متفق نہیں', 'score': 1.0},
            {'id': '2', 'text': 'Disagree', 'text_urdu': 'متفق نہیں', 'score': 2.0},
            {'id': '3', 'text': 'Neutral', 'text_urdu': 'غیر جانبدار', 'score': 3.0},
            {'id': '4', 'text': 'Agree', 'text_urdu': 'متفق ہوں', 'score': 4.0},
            {'id': '5', 'text': 'Strongly Agree', 'text_urdu': 'مکمل متفق ہوں', 'score': 5.0}
        ]
    },
    {
        'question_id': uuid.UUID('7b19a102-2222-4000-8000-000000000008'),
        'text': 'I listen empathetically when peers confide their personal worries and help mediate peaceful disagreements between friends.',
        'text_urdu': 'جب دوست اپنی پریشانیاں بیان کریں تو میں ہمدردی سے سنتا ہوں اور ان کے باہمی جھگڑے حل کروانے میں مدد کرتا ہوں۔',
        'type': Question.TypeChoice.LIKERT,
        'category': Question.CategoryChoice.INTEREST,
        'dimension': 'RIASEC_Social',
        'target_audience': Question.TargetAudienceChoice.MATRIC,
        'order': 44,
        'options': [
            {'id': '1', 'text': 'Strongly Disagree', 'text_urdu': 'بالکل متفق نہیں', 'score': 1.0},
            {'id': '2', 'text': 'Disagree', 'text_urdu': 'متفق نہیں', 'score': 2.0},
            {'id': '3', 'text': 'Neutral', 'text_urdu': 'غیر جانبدار', 'score': 3.0},
            {'id': '4', 'text': 'Agree', 'text_urdu': 'متفق ہوں', 'score': 4.0},
            {'id': '5', 'text': 'Strongly Agree', 'text_urdu': 'مکمل متفق ہوں', 'score': 5.0}
        ]
    },

    # --- ENTERPRISING (4 Items) ---
    {
        'question_id': uuid.UUID('3bf848a6-4d8d-4831-ab09-7879c77479c0'),
        'text': 'I enjoy pitching innovative ideas, leading project teams, negotiating agreements, and persuading groups toward ambitious goals.',
        'text_urdu': 'مجھے نئی کاروباری تجاویز دینا، قیادت کرنا اور لوگوں کو اپنے وژن پر قائل کرنا اچھا لگتا ہے۔',
        'type': Question.TypeChoice.LIKERT,
        'category': Question.CategoryChoice.INTEREST,
        'dimension': 'RIASEC_Enterprising',
        'target_audience': Question.TargetAudienceChoice.MATRIC,
        'order': 45,
        'options': [
            {'id': '1', 'text': 'Strongly Disagree', 'text_urdu': 'بالکل متفق نہیں', 'score': 1.0},
            {'id': '2', 'text': 'Disagree', 'text_urdu': 'متفق نہیں', 'score': 2.0},
            {'id': '3', 'text': 'Neutral', 'text_urdu': 'غیر جانبدار', 'score': 3.0},
            {'id': '4', 'text': 'Agree', 'text_urdu': 'متفق ہوں', 'score': 4.0},
            {'id': '5', 'text': 'Strongly Agree', 'text_urdu': 'مکمل متفق ہوں', 'score': 5.0}
        ]
    },
    {
        'question_id': uuid.UUID('7b19a102-2222-4000-8000-000000000009'),
        'text': 'I like taking initiative to organize school events, manage fundraising drives, and delegate responsibilities to committee members.',
        'text_urdu': 'مجھے اسکول کے فنکشنز کا انتظام سنبھالنا، چندہ جمع کرنے کی مہم چلانا اور ٹیم ممبرز کو ذمے داریاں سونپنا اچھا لگتا ہے۔',
        'type': Question.TypeChoice.LIKERT,
        'category': Question.CategoryChoice.INTEREST,
        'dimension': 'RIASEC_Enterprising',
        'target_audience': Question.TargetAudienceChoice.MATRIC,
        'order': 46,
        'options': [
            {'id': '1', 'text': 'Strongly Disagree', 'text_urdu': 'بالکل متفق نہیں', 'score': 1.0},
            {'id': '2', 'text': 'Disagree', 'text_urdu': 'متفق نہیں', 'score': 2.0},
            {'id': '3', 'text': 'Neutral', 'text_urdu': 'غیر جانبدار', 'score': 3.0},
            {'id': '4', 'text': 'Agree', 'text_urdu': 'متفق ہوں', 'score': 4.0},
            {'id': '5', 'text': 'Strongly Agree', 'text_urdu': 'مکمل متفق ہوں', 'score': 5.0}
        ]
    },
    {
        'question_id': uuid.UUID('7b19a102-2222-4000-8000-000000000010'),
        'text': 'I am interested in exploring commercial business ideas, analyzing market supply and demand, and launching an entrepreneurial venture.',
        'text_urdu': 'مجھے کاروباری مواقع تلاش کرنے، مارکیٹ میں اشیاء کی طلب و رسد سمجھنے اور اپنا کاروبار شروع کرنے میں دلچسپی ہے۔',
        'type': Question.TypeChoice.LIKERT,
        'category': Question.CategoryChoice.INTEREST,
        'dimension': 'RIASEC_Enterprising',
        'target_audience': Question.TargetAudienceChoice.MATRIC,
        'order': 47,
        'options': [
            {'id': '1', 'text': 'Strongly Disagree', 'text_urdu': 'بالکل متفق نہیں', 'score': 1.0},
            {'id': '2', 'text': 'Disagree', 'text_urdu': 'متفق نہیں', 'score': 2.0},
            {'id': '3', 'text': 'Neutral', 'text_urdu': 'غیر جانبدار', 'score': 3.0},
            {'id': '4', 'text': 'Agree', 'text_urdu': 'متفق ہوں', 'score': 4.0},
            {'id': '5', 'text': 'Strongly Agree', 'text_urdu': 'مکمل متفق ہوں', 'score': 5.0}
        ]
    },
    {
        'question_id': uuid.UUID('7b19a102-2222-4000-8000-000000000011'),
        'text': 'I feel confident participating in speech debates, presenting arguments in front of large audiences, and defending a policy position.',
        'text_urdu': 'مجھے تقریری مقابلوں اور مباحثوں میں حصہ لینا اور مجمع کے سامنے پر اعتماد انداز میں دلائل پیش کرنا پسند ہے۔',
        'type': Question.TypeChoice.LIKERT,
        'category': Question.CategoryChoice.INTEREST,
        'dimension': 'RIASEC_Enterprising',
        'target_audience': Question.TargetAudienceChoice.MATRIC,
        'order': 48,
        'options': [
            {'id': '1', 'text': 'Strongly Disagree', 'text_urdu': 'بالکل متفق نہیں', 'score': 1.0},
            {'id': '2', 'text': 'Disagree', 'text_urdu': 'متفق نہیں', 'score': 2.0},
            {'id': '3', 'text': 'Neutral', 'text_urdu': 'غیر جانبدار', 'score': 3.0},
            {'id': '4', 'text': 'Agree', 'text_urdu': 'متفق ہوں', 'score': 4.0},
            {'id': '5', 'text': 'Strongly Agree', 'text_urdu': 'مکمل متفق ہوں', 'score': 5.0}
        ]
    },

    # --- CONVENTIONAL (4 Items) ---
    {
        'question_id': uuid.UUID('fa971aad-d71e-4575-aa56-dec0ee746376'),
        'text': 'I appreciate structured financial data, spreadsheet calculations, strict standard operating procedures, and systematic documentation.',
        'text_urdu': 'مجھے منظم مالیاتی حساب کتاب، باقاعدہ اصول و ضوابط اور ڈیٹا کی درست ترسیل پسند ہے۔',
        'type': Question.TypeChoice.LIKERT,
        'category': Question.CategoryChoice.INTEREST,
        'dimension': 'RIASEC_Conventional',
        'target_audience': Question.TargetAudienceChoice.MATRIC,
        'order': 49,
        'options': [
            {'id': '1', 'text': 'Strongly Disagree', 'text_urdu': 'بالکل متفق نہیں', 'score': 1.0},
            {'id': '2', 'text': 'Disagree', 'text_urdu': 'متفق نہیں', 'score': 2.0},
            {'id': '3', 'text': 'Neutral', 'text_urdu': 'غیر جانبدار', 'score': 3.0},
            {'id': '4', 'text': 'Agree', 'text_urdu': 'متفق ہوں', 'score': 4.0},
            {'id': '5', 'text': 'Strongly Agree', 'text_urdu': 'مکمل متفق ہوں', 'score': 5.0}
        ]
    },
    {
        'question_id': uuid.UUID('7b19a102-2222-4000-8000-000000000012'),
        'text': 'I like keeping my study materials, files, notebooks, and digital documents neatly organized into clear, labeled categories.',
        'text_urdu': 'مجھے اپنے پڑھائی کے نوٹس، فائلیں اور کتابیں ترتیب سے رکھنا اور واضح لیبلز لگا کر سنبھالنا اچھا لگتا ہے۔',
        'type': Question.TypeChoice.LIKERT,
        'category': Question.CategoryChoice.INTEREST,
        'dimension': 'RIASEC_Conventional',
        'target_audience': Question.TargetAudienceChoice.MATRIC,
        'order': 50,
        'options': [
            {'id': '1', 'text': 'Strongly Disagree', 'text_urdu': 'بالکل متفق نہیں', 'score': 1.0},
            {'id': '2', 'text': 'Disagree', 'text_urdu': 'متفق نہیں', 'score': 2.0},
            {'id': '3', 'text': 'Neutral', 'text_urdu': 'غیر جانبدار', 'score': 3.0},
            {'id': '4', 'text': 'Agree', 'text_urdu': 'متفق ہوں', 'score': 4.0},
            {'id': '5', 'text': 'Strongly Agree', 'text_urdu': 'مکمل متفق ہوں', 'score': 5.0}
        ]
    },
    {
        'question_id': uuid.UUID('7b19a102-2222-4000-8000-000000000013'),
        'text': 'I enjoy checking expense receipts, balancing account registers, and verifying that every calculation is error-free.',
        'text_urdu': 'مجھے حسابات کے بل اور رسیدیں چیک کرنا اور یہ تسلی کرنا پسند ہے کہ کوئی حسابی غلطی باقی نہ رہے۔',
        'type': Question.TypeChoice.LIKERT,
        'category': Question.CategoryChoice.INTEREST,
        'dimension': 'RIASEC_Conventional',
        'target_audience': Question.TargetAudienceChoice.MATRIC,
        'order': 51,
        'options': [
            {'id': '1', 'text': 'Strongly Disagree', 'text_urdu': 'بالکل متفق نہیں', 'score': 1.0},
            {'id': '2', 'text': 'Disagree', 'text_urdu': 'متفق نہیں', 'score': 2.0},
            {'id': '3', 'text': 'Neutral', 'text_urdu': 'غیر جانبدار', 'score': 3.0},
            {'id': '4', 'text': 'Agree', 'text_urdu': 'متفق ہوں', 'score': 4.0},
            {'id': '5', 'text': 'Strongly Agree', 'text_urdu': 'مکمل متفق ہوں', 'score': 5.0}
        ]
    },
    {
        'question_id': uuid.UUID('7b19a102-2222-4000-8000-000000000014'),
        'text': 'I perform best when given clear, well-structured guidelines and definite schedules rather than vague, open-ended assignments.',
        'text_urdu': 'جب مجھے واضح اصول اور باقاعدہ ٹائم ٹیبل دیا جائے تو میں غیر واضح کاموں کے مقابلے میں زیادہ بہتر کارکردگی دکھاتا ہوں۔',
        'type': Question.TypeChoice.LIKERT,
        'category': Question.CategoryChoice.INTEREST,
        'dimension': 'RIASEC_Conventional',
        'target_audience': Question.TargetAudienceChoice.MATRIC,
        'order': 52,
        'options': [
            {'id': '1', 'text': 'Strongly Disagree', 'text_urdu': 'بالکل متفق نہیں', 'score': 1.0},
            {'id': '2', 'text': 'Disagree', 'text_urdu': 'متفق نہیں', 'score': 2.0},
            {'id': '3', 'text': 'Neutral', 'text_urdu': 'غیر جانبدار', 'score': 3.0},
            {'id': '4', 'text': 'Agree', 'text_urdu': 'متفق ہوں', 'score': 4.0},
            {'id': '5', 'text': 'Strongly Agree', 'text_urdu': 'مکمل متفق ہوں', 'score': 5.0}
        ]
    },

    # ==========================================================================
    # SECTION 3: ACADEMIC & SUBJECT INTERESTS (10 ITEMS)
    # Measuring genuine affinity for disciplines separately from exam grades
    # ==========================================================================
    {
        'question_id': uuid.UUID('7b19a103-3333-4000-8000-000000000001'),
        'text': 'I genuinely enjoy studying Mathematics, discovering geometric patterns, and solving algebraic equations.',
        'text_urdu': 'مجھے ریاضی پڑھنا، ہندسی نمونے سمجھنا اور الجبرا کی مساواتیں حل کرنا سچ مچ اچھا لگتا ہے۔',
        'type': Question.TypeChoice.LIKERT,
        'category': Question.CategoryChoice.ACADEMIC,
        'dimension': 'Subject_Mathematics',
        'target_audience': Question.TargetAudienceChoice.MATRIC,
        'order': 53,
        'options': [
            {'id': '1', 'text': 'Strongly Disagree', 'text_urdu': 'بالکل متفق نہیں', 'score': 1.0},
            {'id': '2', 'text': 'Disagree', 'text_urdu': 'متفق نہیں', 'score': 2.0},
            {'id': '3', 'text': 'Neutral', 'text_urdu': 'غیر جانبدار', 'score': 3.0},
            {'id': '4', 'text': 'Agree', 'text_urdu': 'متفق ہوں', 'score': 4.0},
            {'id': '5', 'text': 'Strongly Agree', 'text_urdu': 'مکمل متفق ہوں', 'score': 5.0}
        ]
    },
    {
        'question_id': uuid.UUID('7b19a103-3333-4000-8000-000000000002'),
        'text': 'I enjoy studying Physics concepts such as forces, electricity, sound waves, motion, and energy conservation.',
        'text_urdu': 'مجھے فزکس کے اسباق جیسے قوت، برقی رو، روشنی، حرارت اور توانائی کی منتقلی پڑھنا پسند ہے۔',
        'type': Question.TypeChoice.LIKERT,
        'category': Question.CategoryChoice.ACADEMIC,
        'dimension': 'Subject_Physics',
        'target_audience': Question.TargetAudienceChoice.MATRIC,
        'order': 54,
        'options': [
            {'id': '1', 'text': 'Strongly Disagree', 'text_urdu': 'بالکل متفق نہیں', 'score': 1.0},
            {'id': '2', 'text': 'Disagree', 'text_urdu': 'متفق نہیں', 'score': 2.0},
            {'id': '3', 'text': 'Neutral', 'text_urdu': 'غیر جانبدار', 'score': 3.0},
            {'id': '4', 'text': 'Agree', 'text_urdu': 'متفق ہوں', 'score': 4.0},
            {'id': '5', 'text': 'Strongly Agree', 'text_urdu': 'مکمل متفق ہوں', 'score': 5.0}
        ]
    },
    {
        'question_id': uuid.UUID('7b19a103-3333-4000-8000-000000000003'),
        'text': 'I am deeply fascinated by Biology topics such as human organ systems, cellular structures, genetics, and plant life.',
        'text_urdu': 'مجھے بائیولوجی کے موضوعات جیسے انسانی اعضاء کا نظام، خلیات کی ساخت، جینیات اور پودوں کی زندگی میں گہری دلچسپی ہے۔',
        'type': Question.TypeChoice.LIKERT,
        'category': Question.CategoryChoice.ACADEMIC,
        'dimension': 'Subject_Biology',
        'target_audience': Question.TargetAudienceChoice.MATRIC,
        'order': 55,
        'options': [
            {'id': '1', 'text': 'Strongly Disagree', 'text_urdu': 'بالکل متفق نہیں', 'score': 1.0},
            {'id': '2', 'text': 'Disagree', 'text_urdu': 'متفق نہیں', 'score': 2.0},
            {'id': '3', 'text': 'Neutral', 'text_urdu': 'غیر جانبدار', 'score': 3.0},
            {'id': '4', 'text': 'Agree', 'text_urdu': 'متفق ہوں', 'score': 4.0},
            {'id': '5', 'text': 'Strongly Agree', 'text_urdu': 'مکمل متفق ہوں', 'score': 5.0}
        ]
    },
    {
        'question_id': uuid.UUID('7b19a103-3333-4000-8000-000000000004'),
        'text': 'I enjoy Chemistry topics such as chemical equations, atomic bonding, the periodic table, and chemical solutions.',
        'text_urdu': 'مجھے کیمسٹری کے موضوعات جیسے کیمیائی مساواتیں، ایٹمی ساخت، دوری جدول اور محلول بنانا اچھے لگتے ہیں۔',
        'type': Question.TypeChoice.LIKERT,
        'category': Question.CategoryChoice.ACADEMIC,
        'dimension': 'Subject_Chemistry',
        'target_audience': Question.TargetAudienceChoice.MATRIC,
        'order': 56,
        'options': [
            {'id': '1', 'text': 'Strongly Disagree', 'text_urdu': 'بالکل متفق نہیں', 'score': 1.0},
            {'id': '2', 'text': 'Disagree', 'text_urdu': 'متفق نہیں', 'score': 2.0},
            {'id': '3', 'text': 'Neutral', 'text_urdu': 'غیر جانبدار', 'score': 3.0},
            {'id': '4', 'text': 'Agree', 'text_urdu': 'متفق ہوں', 'score': 4.0},
            {'id': '5', 'text': 'Strongly Agree', 'text_urdu': 'مکمل متفق ہوں', 'score': 5.0}
        ]
    },
    {
        'question_id': uuid.UUID('7b19a103-3333-4000-8000-000000000005'),
        'text': 'I enjoy learning Computer Science, writing simple code, understanding algorithms, and exploring digital software.',
        'text_urdu': 'مجھے کمپیوٹر سائنس پڑھنا، کوڈنگ سیکھنا، الگورتھم سمجھنا اور جدید سافٹ ویئر چلانا پسند ہے۔',
        'type': Question.TypeChoice.LIKERT,
        'category': Question.CategoryChoice.ACADEMIC,
        'dimension': 'Subject_ComputerScience',
        'target_audience': Question.TargetAudienceChoice.MATRIC,
        'order': 57,
        'options': [
            {'id': '1', 'text': 'Strongly Disagree', 'text_urdu': 'بالکل متفق نہیں', 'score': 1.0},
            {'id': '2', 'text': 'Disagree', 'text_urdu': 'متفق نہیں', 'score': 2.0},
            {'id': '3', 'text': 'Neutral', 'text_urdu': 'غیر جانبدار', 'score': 3.0},
            {'id': '4', 'text': 'Agree', 'text_urdu': 'متفق ہوں', 'score': 4.0},
            {'id': '5', 'text': 'Strongly Agree', 'text_urdu': 'مکمل متفق ہوں', 'score': 5.0}
        ]
    },
    {
        'question_id': uuid.UUID('7b19a103-3333-4000-8000-000000000006'),
        'text': 'I enjoy English and Urdu language studies, reading classical literature, writing essays, and verbal communication.',
        'text_urdu': 'مجھے اردو اور انگریزی زبان و ادب پڑھنا، مضامین لکھنا اور مؤثر انداز میں بات چیت کرنا پسند ہے۔',
        'type': Question.TypeChoice.LIKERT,
        'category': Question.CategoryChoice.ACADEMIC,
        'dimension': 'Subject_Languages',
        'target_audience': Question.TargetAudienceChoice.MATRIC,
        'order': 58,
        'options': [
            {'id': '1', 'text': 'Strongly Disagree', 'text_urdu': 'بالکل متفق نہیں', 'score': 1.0},
            {'id': '2', 'text': 'Disagree', 'text_urdu': 'متفق نہیں', 'score': 2.0},
            {'id': '3', 'text': 'Neutral', 'text_urdu': 'غیر جانبدار', 'score': 3.0},
            {'id': '4', 'text': 'Agree', 'text_urdu': 'متفق ہوں', 'score': 4.0},
            {'id': '5', 'text': 'Strongly Agree', 'text_urdu': 'مکمل متفق ہوں', 'score': 5.0}
        ]
    },
    {
        'question_id': uuid.UUID('7b19a103-3333-4000-8000-000000000007'),
        'text': 'I find commerce topics such as accounting books, banking procedures, trade, and economic principles fascinating.',
        'text_urdu': 'مجھے کامرس، کھاتہ داری (Accounting)، بینکنگ، تجارت اور معیشت کے موضوعات میں گہری دلچسپی ہے۔',
        'type': Question.TypeChoice.LIKERT,
        'category': Question.CategoryChoice.ACADEMIC,
        'dimension': 'Subject_Commerce',
        'target_audience': Question.TargetAudienceChoice.MATRIC,
        'order': 59,
        'options': [
            {'id': '1', 'text': 'Strongly Disagree', 'text_urdu': 'بالکل متفق نہیں', 'score': 1.0},
            {'id': '2', 'text': 'Disagree', 'text_urdu': 'متفق نہیں', 'score': 2.0},
            {'id': '3', 'text': 'Neutral', 'text_urdu': 'غیر جانبدار', 'score': 3.0},
            {'id': '4', 'text': 'Agree', 'text_urdu': 'متفق ہوں', 'score': 4.0},
            {'id': '5', 'text': 'Strongly Agree', 'text_urdu': 'مکمل متفق ہوں', 'score': 5.0}
        ]
    },
    {
        'question_id': uuid.UUID('7b19a103-3333-4000-8000-000000000008'),
        'text': 'I enjoy studying Pakistan Studies, world history, legal justice systems, civics, and how human societies govern themselves.',
        'text_urdu': 'مجھے مطالعہ پاکستان، تاریخ، عدالتی نظام، شہریت (Civics) اور معاشرتی اصولوں کا مطالعہ اچھا لگتا ہے۔',
        'type': Question.TypeChoice.LIKERT,
        'category': Question.CategoryChoice.ACADEMIC,
        'dimension': 'Subject_SocialSciences',
        'target_audience': Question.TargetAudienceChoice.MATRIC,
        'order': 60,
        'options': [
            {'id': '1', 'text': 'Strongly Disagree', 'text_urdu': 'بالکل متفق نہیں', 'score': 1.0},
            {'id': '2', 'text': 'Disagree', 'text_urdu': 'متفق نہیں', 'score': 2.0},
            {'id': '3', 'text': 'Neutral', 'text_urdu': 'غیر جانبدار', 'score': 3.0},
            {'id': '4', 'text': 'Agree', 'text_urdu': 'متفق ہوں', 'score': 4.0},
            {'id': '5', 'text': 'Strongly Agree', 'text_urdu': 'مکمل متفق ہوں', 'score': 5.0}
        ]
    },
    {
        'question_id': uuid.UUID('7b19a103-3333-4000-8000-000000000009'),
        'text': 'I enjoy drawing building plans, analyzing architectural models, and studying physical spaces, landscapes, and interior design.',
        'text_urdu': 'مجھے عمارتی نقشے بنانا، ماڈلز کا جائزہ لینا اور عمارتوں کے اندرونی ڈیزائن کو سمجھنا پسند ہے۔',
        'type': Question.TypeChoice.LIKERT,
        'category': Question.CategoryChoice.ACADEMIC,
        'dimension': 'Subject_ArchitectureArt',
        'target_audience': Question.TargetAudienceChoice.MATRIC,
        'order': 61,
        'options': [
            {'id': '1', 'text': 'Strongly Disagree', 'text_urdu': 'بالکل متفق نہیں', 'score': 1.0},
            {'id': '2', 'text': 'Disagree', 'text_urdu': 'متفق نہیں', 'score': 2.0},
            {'id': '3', 'text': 'Neutral', 'text_urdu': 'غیر جانبدار', 'score': 3.0},
            {'id': '4', 'text': 'Agree', 'text_urdu': 'متفق ہوں', 'score': 4.0},
            {'id': '5', 'text': 'Strongly Agree', 'text_urdu': 'مکمل متفق ہوں', 'score': 5.0}
        ]
    },
    {
        'question_id': uuid.UUID('7b19a103-3333-4000-8000-000000000010'),
        'text': 'I enjoy practical vocational learning such as electronics repair, mechanical drafting, automotive care, or technical workshops.',
        'text_urdu': 'مجھے فنی و پیشہ ورانہ مہارتیں جیسے الیکٹرانکس کی مرمت، مکینیکل ڈرائنگ اور ورکشاپ کا عملی کام سیکھنا پسند ہے۔',
        'type': Question.TypeChoice.LIKERT,
        'category': Question.CategoryChoice.ACADEMIC,
        'dimension': 'Subject_TechnicalVocational',
        'target_audience': Question.TargetAudienceChoice.MATRIC,
        'order': 62,
        'options': [
            {'id': '1', 'text': 'Strongly Disagree', 'text_urdu': 'بالکل متفق نہیں', 'score': 1.0},
            {'id': '2', 'text': 'Disagree', 'text_urdu': 'متفق نہیں', 'score': 2.0},
            {'id': '3', 'text': 'Neutral', 'text_urdu': 'غیر جانبدار', 'score': 3.0},
            {'id': '4', 'text': 'Agree', 'text_urdu': 'متفق ہوں', 'score': 4.0},
            {'id': '5', 'text': 'Strongly Agree', 'text_urdu': 'مکمل متفق ہوں', 'score': 5.0}
        ]
    },

    # ==========================================================================
    # SECTION 4: CAREER AWARENESS & LEARNING PREFERENCES (6 ITEMS)
    # Formative decision-making indicators without penalized right/wrong keys
    # ==========================================================================
    {
        'question_id': uuid.UUID('7b19a104-4444-4000-8000-000000000001'),
        'text': 'Which primary working environment appeals to you most for your future professional life?',
        'text_urdu': 'مستقبل کی عملی زندگی کے لیے آپ کو کس قسم کا ماحول سب سے زیادہ پسند ہے؟',
        'type': Question.TypeChoice.MCQ,
        'category': Question.CategoryChoice.PERSONALITY,
        'dimension': 'Pref_WorkEnvironment',
        'target_audience': Question.TargetAudienceChoice.MATRIC,
        'order': 63,
        'options': [
            {'id': 'A', 'text': 'A research laboratory, diagnostic hospital, or healthcare clinic', 'text_urdu': 'سائنسی ریسرچ لیب یا ہسپتال کا طبی ماحول'},
            {'id': 'B', 'text': 'A modern tech office, software development studio, or design firm', 'text_urdu': 'سافٹ ویئر اسٹوڈیو یا جدید ٹیکنالوجی کا دفتر'},
            {'id': 'C', 'text': 'An engineering construction site, industrial manufacturing plant, or outdoor field', 'text_urdu': 'انجینئرنگ کنسٹرکشن سائٹ، صنعتی پلانٹ یا فیلڈ کا کام'},
            {'id': 'D', 'text': 'A corporate business office, financial bank, or legal courtroom', 'text_urdu': 'کارپوریٹ بزنس آفس، بینک یا قانونی عدالت'}
        ]
    },
    {
        'question_id': uuid.UUID('7b19a104-4444-4000-8000-000000000002'),
        'text': 'Do you prefer learning through hands-on practical implementation or theoretical conceptual analysis?',
        'text_urdu': 'آپ عملی کام کر کے سیکھنے کو ترجیح دیتے ہیں یا کتابی و نظریاتی تجزیے کو؟',
        'type': Question.TypeChoice.MCQ,
        'category': Question.CategoryChoice.PERSONALITY,
        'dimension': 'Pref_LearningStyle',
        'target_audience': Question.TargetAudienceChoice.MATRIC,
        'order': 64,
        'options': [
            {'id': 'A', 'text': 'Primarily practical: building, testing, drawing, or repairing tangible physical things', 'text_urdu': 'بنیادی طور پر عملی: اوزاروں، مشینوں یا کوڈنگ سے کام بنانا'},
            {'id': 'B', 'text': 'A balanced mix of classroom theory and practical laboratory experiments', 'text_urdu': 'نظریہ اور عملی کام کا متوازن امتزاج'},
            {'id': 'C', 'text': 'Primarily conceptual: studying theories, reading case laws, and analyzing policies', 'text_urdu': 'بنیادی طور پر نظریاتی: اصول و قوانین، کیس اسٹڈیز اور فلسفہ پڑھنا'}
        ]
    },
    {
        'question_id': uuid.UUID('7b19a104-4444-4000-8000-000000000003'),
        'text': 'How do you prefer to approach significant academic or extracurricular projects?',
        'text_urdu': 'کسی اہم تعلیمی یا غیر نصابی پراجیکٹ کے دوران آپ کا پسندیدہ انداز کیا ہوتا ہے؟',
        'type': Question.TypeChoice.MCQ,
        'category': Question.CategoryChoice.PERSONALITY,
        'dimension': 'Pref_CollaborationMode',
        'target_audience': Question.TargetAudienceChoice.MATRIC,
        'order': 65,
        'options': [
            {'id': 'A', 'text': 'Independently, having full creative and analytical autonomy over my work', 'text_urdu': 'تنہا کام کرنا، تاکہ اپنی رفتار اور آزادی سے نتیجہ حاصل کر سکوں'},
            {'id': 'B', 'text': 'In a close collaborative team where tasks and ideas are shared mutually', 'text_urdu': 'ساتھیوں کے ساتھ ٹیم میں مل جل کر کام بانٹنا'},
            {'id': 'C', 'text': 'In a leadership capacity, coordinating schedules, delegating tasks, and motivating others', 'text_urdu': 'بطورِ لیڈر، منصوبے کی نگرانی کرنا اور دوسروں کی رہنمائی کرنا'}
        ]
    },
    {
        'question_id': uuid.UUID('7b19a104-4444-4000-8000-000000000004'),
        'text': 'Which long-term outcome would give you the deepest sense of accomplishment in your future career?',
        'text_urdu': 'مستقبل کے کیریئر میں کون سا نتیجہ آپ کو سب سے زیادہ دلی اطمینان بخشے گا؟',
        'type': Question.TypeChoice.MCQ,
        'category': Question.CategoryChoice.PERSONALITY,
        'dimension': 'Pref_PrimaryMotivation',
        'target_audience': Question.TargetAudienceChoice.MATRIC,
        'order': 66,
        'options': [
            {'id': 'A', 'text': 'Developing innovative technology, inventing software, or designing monumental buildings', 'text_urdu': 'نئی ٹیکنالوجی بنانا، سافٹ ویئر ایجاد کرنا یا عمارتیں ڈیزائن کرنا'},
            {'id': 'B', 'text': 'Treating patients, curing illnesses, or educating and mentoring younger generations', 'text_urdu': 'مریضوں کا علاج کرنا، بیماریاں دور کرنا یا نئی نسل کو تعلیم دینا'},
            {'id': 'C', 'text': 'Building an ethical, highly successful corporate business and managing financial investments', 'text_urdu': 'ایک کامیاب کاروبار قائم کرنا اور مالیاتی سرمایہ کاری سنبھالنا'},
            {'id': 'D', 'text': 'Defending the rule of law, protecting fundamental rights, and shaping public policies', 'text_urdu': 'انصاف اور آئین کی حفاظت کرنا اور ملکی قوانین کی بہتری میں حصہ لینا'}
        ]
    },
    {
        'question_id': uuid.UUID('a9fe0fdc-ef54-4dbe-80a7-f7e81cb96a26'),
        'text': 'Looking ahead to Class 11 (Intermediate) admission, which academic stream currently feels most aligned with your goals?',
        'text_urdu': 'کلاس 11 (انٹرمیڈیٹ) میں داخلے کے لیے فی الوقت کون سا تعلیمی گروپ آپ کے مستقبل کے ارادوں کے سب سے قریب لگتا ہے؟',
        'type': Question.TypeChoice.MCQ,
        'category': Question.CategoryChoice.PERSONALITY,
        'dimension': 'Pref_StreamAspiration',
        'target_audience': Question.TargetAudienceChoice.MATRIC,
        'order': 67,
        'options': [
            {'id': 'A', 'text': 'Science Pre-Engineering (Math, Physics, Chemistry)', 'text_urdu': 'پری انجینئرنگ (ریاضی، فزکس، کیمسٹری)'},
            {'id': 'B', 'text': 'Science Pre-Medical (Biology, Physics, Chemistry)', 'text_urdu': 'پری میڈیکل (بائیولوجی، فزکس، کیمسٹری)'},
            {'id': 'C', 'text': 'Computer Science / ICS (Math, Physics/Stats, Computer)', 'text_urdu': 'کمپیوٹر سائنس / ICS (ریاضی، فزکس، کمپیوٹر)'},
            {'id': 'D', 'text': 'Commerce / I.Com (Accounting, Banking, Business Math)', 'text_urdu': 'کامرس / I.Com (اکاؤنٹنگ، بینکاری، بزنس میتھ)'},
            {'id': 'E', 'text': 'Humanities / Arts / FA (Civics, History, Psychology, Languages)', 'text_urdu': 'آرٹس و انسانیات / FA (سوکس، تاریخ، نفسیات، زبانیں)'},
            {'id': 'F', 'text': 'Technical Diploma / DAE or Home Economics', 'text_urdu': 'ٹیکنیکل ڈپلومہ (DAE) یا ہوم اکنامکس'}
        ]
    },
    {
        'question_id': uuid.UUID('6af4d27e-3743-4347-b062-4c342e9e8069'),
        'text': 'When deciding your Class 11 Intermediate group after Matric, which factor should serve as the most reliable basis for your decision?',
        'text_urdu': 'میٹرک کے بعد کلاس 11 کے تعلیمی گروپ کا فیصلہ کرتے وقت سب سے اہم اور درست بنیاد کیا ہونی چاہیے؟',
        'type': Question.TypeChoice.MCQ,
        'category': Question.CategoryChoice.PERSONALITY,
        'dimension': 'Pref_CareerDecisionMaturity',
        'target_audience': Question.TargetAudienceChoice.MATRIC,
        'order': 68,
        'options': [
            {'id': 'A', 'text': 'Selecting a field solely because my closest friends or relatives are choosing it', 'text_urdu': 'صرف اس لیے منتخب کرنا کیونکہ دوست یا رشتہ دار وہاں جا رہے ہیں'},
            {'id': 'B', 'text': 'Evaluating my genuine interests, demonstrated academic strengths, and verified college eligibility rules', 'text_urdu': 'اپنی حقیقی دلچسپیوں، تعلیمی صلاحیتوں اور کالج کے باقاعدہ داخلہ اصولوں کا جائزہ لے کر فیصلہ کرنا'},
            {'id': 'C', 'text': 'Choosing blindly based only on whatever field is currently popular on social media', 'text_urdu': 'صرف وقتی رجحان یا مقبولیت کی بنیاد پر بغیر معلومات کے منتخب کرنا'}
        ]
    }
]
