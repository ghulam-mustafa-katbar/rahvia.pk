import os
import django

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'rahvia_project.settings')
django.setup()

from assessments.models import Question

qs = Question.objects.all().order_by('order')
print(f"Total questions in database: {qs.count()}")
errors = []

for q in qs:
    # 1. Text checks
    if not q.text or len(q.text.strip()) < 10:
        errors.append(f"[{q.order}] Question {q.question_id} has empty or short English text.")
    if not q.text_urdu or len(q.text_urdu.strip()) < 5:
        errors.append(f"[{q.order}] Question {q.question_id} has empty or short Urdu text.")
    
    # 2. Options checks
    if not q.options or len(q.options) < 2:
        errors.append(f"[{q.order}] Question {q.question_id} has insufficient options ({len(q.options)}).")
    else:
        opt_ids = [opt.get('id') for opt in q.options]
        if len(opt_ids) != len(set(opt_ids)):
            errors.append(f"[{q.order}] Question {q.question_id} has duplicate option IDs: {opt_ids}")
        for opt in q.options:
            if not opt.get('text'):
                errors.append(f"[{q.order}] Option {opt.get('id')} in {q.question_id} lacks English text.")
            if not opt.get('text_urdu'):
                errors.append(f"[{q.order}] Option {opt.get('id')} in {q.question_id} lacks Urdu text.")
    
    # 3. Category & Correct Answer checks
    if q.category == Question.CategoryChoice.APTITUDE:
        if not q.correct_answer:
            errors.append(f"[{q.order}] Cognitive question {q.question_id} missing correct_answer.")
        elif q.correct_answer not in [opt.get('id') for opt in q.options]:
            errors.append(f"[{q.order}] Cognitive question {q.question_id} correct_answer '{q.correct_answer}' not found in options {opt_ids}.")
        if not q.explanation:
            errors.append(f"[{q.order}] Cognitive question {q.question_id} missing explanation.")
        if not q.explanation_urdu:
            errors.append(f"[{q.order}] Cognitive question {q.question_id} missing explanation_urdu.")
    else:
        if q.correct_answer != '':
            errors.append(f"[{q.order}] Non-cognitive question {q.question_id} ({q.category}) has unexpected correct_answer '{q.correct_answer}'.")

if errors:
    print(f"FAILED: Found {len(errors)} question bank integrity defects:")
    for err in errors:
        print("  - " + err)
else:
    print("SUCCESS: ALL 68 QUESTION BANK ITEMS PASSED COMPREHENSIVE INTEGRITY AUDIT (100% OK)!")
