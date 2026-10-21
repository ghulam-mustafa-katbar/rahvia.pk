import math
from typing import Dict, Any, List
from django.utils import timezone
from .models import AssessmentSession, Response, DimensionScore, Question

def calculate_percentile_from_pct(percentage: float, mean: float = 60.0, std_dev: float = 16.0) -> float:
    """
    Computes an indicative psychometric percentile rank using standard normal
    cumulative distribution referenced to secondary school student performance distributions.
    This provides comparative reference percentiles and does not constitute a diagnostic clinical norm.
    """
    if std_dev <= 0:
        return 50.0
    z = (percentage - mean) / std_dev
    # Standard normal cumulative distribution approximation (erf based)
    phi = 0.5 * (1.0 + math.erf(z / math.sqrt(2.0)))
    percentile = round(phi * 100.0, 1)
    return max(1.0, min(99.0, percentile))

def process_assessment_submission(assessment: AssessmentSession, answer_items: List[Dict[str, Any]]) -> Dict[str, Any]:
    """
    Processes an assessment submission for Matric (Class 9-10) and Secondary students.
    Transparently segregates:
      1. Cognitive Aptitude items (scored 0 or 1 based on verified answer keys)
      2. RIASEC Interest items (1-5 Likert scale, with reverse scoring support)
      3. Academic Subject Interest items (1-5 Likert scale)
      4. Career Preferences & Work Styles (qualitative indicators)
    """
    question_ids = [item['question_id'] for item in answer_items if 'question_id' in item]
    questions_map = {str(q.question_id): q for q in Question.objects.filter(question_id__in=question_ids)}

    # Reset any previous responses for retry safety
    Response.objects.filter(assessment=assessment).delete()
    DimensionScore.objects.filter(assessment=assessment).delete()

    created_responses = []

    # Category accumulators
    cognitive_aggregates: Dict[str, Dict[str, float]] = {}
    riasec_aggregates: Dict[str, List[float]] = {}
    academic_interests: Dict[str, float] = {}
    career_preferences: Dict[str, str] = {}

    total_cognitive_score = 0.0
    max_cognitive_score = 0.0

    for item in answer_items:
        qid_str = str(item.get('question_id'))
        ans_str = str(item.get('student_answer', '')).strip()
        time_taken = int(item.get('time_taken_seconds', 0))

        question = questions_map.get(qid_str)
        if not question:
            continue

        score_awarded = 0.0
        dim_key = question.dimension or 'GeneralAptitude'

        if question.category == Question.CategoryChoice.INTEREST or question.type == Question.TypeChoice.LIKERT:
            # Parse 1-5 scale rating
            val = 3.0
            matched_opt = None
            for opt in question.options:
                if str(opt.get('id', '')).upper() == ans_str.upper() or str(opt.get('text', '')).upper() == ans_str.upper():
                    matched_opt = opt
                    break

            if matched_opt and 'score' in matched_opt:
                try:
                    val = float(matched_opt['score'])
                except (ValueError, TypeError):
                    val = 3.0
            else:
                try:
                    val = float(ans_str)
                except (ValueError, TypeError):
                    # Check if letter A-E mapped to 1-5
                    letter_map = {'A': 1.0, 'B': 2.0, 'C': 3.0, 'D': 4.0, 'E': 5.0}
                    val = letter_map.get(ans_str.upper(), 3.0)

            # Clamp between 1.0 and 5.0
            val = max(1.0, min(5.0, val))

            # Apply reverse scoring if specified
            if getattr(question, 'is_reverse_scored', False):
                val = 6.0 - val

            score_awarded = val

            if dim_key.startswith('RIASEC_'):
                if dim_key not in riasec_aggregates:
                    riasec_aggregates[dim_key] = []
                riasec_aggregates[dim_key].append(val)
            elif dim_key.startswith('Subject_') or dim_key.startswith('Academic_'):
                academic_interests[dim_key] = val
            else:
                # Generic interest
                if dim_key not in riasec_aggregates:
                    riasec_aggregates[dim_key] = []
                riasec_aggregates[dim_key].append(val)

        elif (
            question.category in [Question.CategoryChoice.PERSONALITY, getattr(Question.CategoryChoice, 'CAREER_PREFERENCE', 'PERSONALITY')]
            or dim_key.startswith('Pref_')
            or dim_key.startswith('Career_')
        ):
            # Qualitative Career Preference / Work Style indicator
            career_preferences[dim_key] = ans_str
            score_awarded = 1.0  # Completion acknowledgment

        else:
            # Cognitive / Aptitude item (Numerical, Logical, Verbal, Spatial, Scientific, Practical)
            max_score_for_q = float(question.correct_answer_weight or 1.0)
            max_cognitive_score += max_score_for_q

            # Verify against answer key
            is_correct = False
            if question.correct_answer and ans_str.strip().upper() == question.correct_answer.strip().upper():
                is_correct = True
            else:
                for opt in question.options:
                    if (str(opt.get('id', '')).upper() == ans_str.upper() or str(opt.get('text', '')).strip() == ans_str.strip()) and opt.get('is_correct'):
                        is_correct = True
                        break

            if is_correct:
                score_awarded = max_score_for_q

            total_cognitive_score += score_awarded

            if dim_key not in cognitive_aggregates:
                cognitive_aggregates[dim_key] = {'raw': 0.0, 'max': 0.0}
            cognitive_aggregates[dim_key]['raw'] += score_awarded
            cognitive_aggregates[dim_key]['max'] += max_score_for_q

        created_responses.append(Response(
            assessment=assessment,
            question=question,
            student_answer=ans_str,
            score_awarded=score_awarded,
            time_taken_seconds=time_taken
        ))

    Response.objects.bulk_create(created_responses)

    # Calculate dimension scores & percentiles for both Cognitive & RIASEC
    dimension_score_objs = []
    dimension_results = {}

    # 1. Cognitive Dimensions
    for dim_name, agg in cognitive_aggregates.items():
        raw = agg['raw']
        max_val = agg['max'] if agg['max'] > 0 else 1.0
        pct = min(100.0, max(0.0, (raw / max_val) * 100.0))
        percentile = calculate_percentile_from_pct(pct)

        dimension_score_objs.append(DimensionScore(
            assessment=assessment,
            dimension_name=dim_name,
            raw_score=round(raw, 2),
            max_possible=round(max_val, 2),
            percentage=round(pct, 1),
            percentile=round(percentile, 1)
        ))
        dimension_results[dim_name] = {
            'raw_score': round(raw, 2),
            'max_possible': round(max_val, 2),
            'percentage': round(pct, 1),
            'percentile': round(percentile, 1),
            'type': 'cognitive'
        }

    # 2. RIASEC Dimensions (scale 1.0 to 5.0 converted to percentage)
    for dim_name, scores in riasec_aggregates.items():
        avg_score = sum(scores) / len(scores) if scores else 3.0
        # Convert 1-5 scale to 0-100%
        pct = round(((avg_score - 1.0) / 4.0) * 100.0, 1)
        percentile = calculate_percentile_from_pct(pct, mean=50.0, std_dev=20.0)

        dimension_score_objs.append(DimensionScore(
            assessment=assessment,
            dimension_name=dim_name,
            raw_score=round(avg_score, 2),
            max_possible=5.0,
            percentage=pct,
            percentile=percentile
        ))
        dimension_results[dim_name] = {
            'raw_score': round(avg_score, 2),
            'max_possible': 5.0,
            'percentage': pct,
            'percentile': percentile,
            'type': 'riasec'
        }

    # 3. Academic Interest Dimensions
    for dim_name, score in academic_interests.items():
        pct = round(((score - 1.0) / 4.0) * 100.0, 1)
        dimension_results[dim_name] = {
            'raw_score': round(score, 2),
            'max_possible': 5.0,
            'percentage': pct,
            'type': 'academic_interest'
        }

    DimensionScore.objects.bulk_create(dimension_score_objs)

    # Finalize assessment session
    assessment.total_score = round(total_cognitive_score, 2)
    assessment.status = AssessmentSession.StatusChoice.COMPLETED
    assessment.completed_at = timezone.now()
    assessment.save()

    return {
        'assessment_id': str(assessment.assessment_id),
        'total_score': assessment.total_score,
        'max_cognitive_score': max_cognitive_score,
        'dimensions': dimension_results,
        'academic_interests': academic_interests,
        'career_preferences': career_preferences,
        'status': assessment.status
    }
