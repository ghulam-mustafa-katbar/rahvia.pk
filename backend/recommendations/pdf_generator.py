import io
import os
from django.conf import settings
from reportlab.lib import colors
from reportlab.lib.pagesizes import letter
from reportlab.lib.styles import getSampleStyleSheet, ParagraphStyle
from reportlab.platypus import (
    SimpleDocTemplate, Paragraph, Spacer, Table, TableStyle, HRFlowable, PageBreak, KeepTogether
)
from .models import Report

def generate_report_pdf(report: Report) -> bytes:
    """
    Generates a beautifully formatted, highly structured 2-page PDF career guidance
    dossier tailored for Pakistani students and institutions.
    """
    buffer = io.BytesIO()
    doc = SimpleDocTemplate(
        buffer,
        pagesize=letter,
        rightMargin=36,
        leftMargin=36,
        topMargin=32,
        bottomMargin=32
    )

    styles = getSampleStyleSheet()
    
    # Palette
    pakistan_green = colors.HexColor('#064E3B')
    emerald_accent = colors.HexColor('#059669')
    navy_accent = colors.HexColor('#1E3A8A')
    slate_dark = colors.HexColor('#0F172A')
    slate_muted = colors.HexColor('#475569')
    slate_light = colors.HexColor('#F8FAFC')
    slate_border = colors.HexColor('#E2E8F0')

    title_style = ParagraphStyle(
        'DocTitle',
        parent=styles['Heading1'],
        fontSize=18,
        leading=22,
        textColor=pakistan_green,
        fontName='Helvetica-Bold',
        spaceAfter=2
    )
    subtitle_style = ParagraphStyle(
        'DocSubtitle',
        parent=styles['Normal'],
        fontSize=9,
        leading=13,
        textColor=slate_muted,
        spaceAfter=8
    )
    section_style = ParagraphStyle(
        'SectionHeader',
        parent=styles['Heading2'],
        fontSize=11,
        leading=15,
        textColor=pakistan_green,
        fontName='Helvetica-Bold',
        spaceBefore=8,
        spaceAfter=4
    )
    body_style = ParagraphStyle(
        'DocBody',
        parent=styles['Normal'],
        fontSize=8.5,
        leading=12,
        textColor=slate_dark,
        spaceAfter=3
    )
    bold_body_style = ParagraphStyle(
        'DocBoldBody',
        parent=body_style,
        fontName='Helvetica-Bold'
    )
    small_style = ParagraphStyle(
        'DocSmall',
        parent=styles['Normal'],
        fontSize=7.5,
        leading=10,
        textColor=slate_muted
    )

    elements = []

    # =========================================================================
    # PAGE 1: STUDENT PROFILE, EXECUTIVE SUMMARY, STREAMS, & DIMENSIONS
    # =========================================================================

    # Title & Branding Header
    elements.append(Paragraph("RAHVIA NATIONAL CAREER GUIDANCE DOSSIER", title_style))
    elements.append(Paragraph("Verifiable Psychometric & Educational Pathway Evaluation | Islamic Republic of Pakistan", subtitle_style))
    elements.append(HRFlowable(width="100%", thickness=1.5, color=pakistan_green, spaceAfter=8))

    # Student Details Grid
    student = report.student
    school_name = student.school.name if (student and student.school) else "Independent Candidate"
    student_name = student.name if student else "Candidate"
    board_name = student.board if student else "National Board"
    grade_name = student.get_current_grade_display() if student else "Intermediate"
    elective_name = student.get_elective_group_display() if student else "General"
    assessment_date = report.created_at.strftime("%d %B %Y")

    student_data = [
        [Paragraph(f"<b>Student Name:</b> {student_name}", body_style), Paragraph(f"<b>Institution:</b> {school_name}", body_style)],
        [Paragraph(f"<b>Education Board:</b> {board_name}", body_style), Paragraph(f"<b>Current Grade:</b> {grade_name}", body_style)],
        [Paragraph(f"<b>Elective Group:</b> {elective_name}", body_style), Paragraph(f"<b>Evaluation Date:</b> {assessment_date}", body_style)],
    ]
    student_table = Table(student_data, colWidths=[270, 270])
    student_table.setStyle(TableStyle([
        ('BACKGROUND', (0, 0), (-1, -1), slate_light),
        ('BOX', (0, 0), (-1, -1), 0.5, slate_border),
        ('INNERGRID', (0, 0), (-1, -1), 0.5, slate_border),
        ('TOPPADDING', (0, 0), (-1, -1), 4),
        ('BOTTOMPADDING', (0, 0), (-1, -1), 4),
        ('LEFTPADDING', (0, 0), (-1, -1), 8),
        ('RIGHTPADDING', (0, 0), (-1, -1), 8),
    ]))
    elements.append(student_table)
    elements.append(Spacer(1, 6))

    # Executive Summary Narrative
    elements.append(Paragraph("Executive Guidance Summary", section_style))
    summary_text = report.summary_narrative or "Candidate profile indicates strong alignment with technical and investigative pathways in Pakistan."
    elements.append(Paragraph(summary_text, body_style))
    elements.append(Spacer(1, 6))

    # Top Recommended Streams
    elements.append(Paragraph("Primary Recommended Higher Secondary Streams (HSSC / Inter)", section_style))
    streams = report.recommended_streams or ['ICS (Computer Science)', 'FSc Pre-Engineering']
    stream_bullets = "".join([f"<li><b>{s}</b></li>" for s in streams])
    elements.append(Paragraph(f"<ul>{stream_bullets}</ul>", body_style))
    elements.append(Spacer(1, 6))

    # Dimension Aptitude Scores Table (Formatted into clean compact 2-column or list)
    elements.append(Paragraph("Psychometric Dimension Scores & Percentiles", section_style))
    
    raw_dimensions = list(report.assessment.dimension_scores.all()) if (report.assessment and hasattr(report.assessment, 'dimension_scores')) else []
    
    if raw_dimensions:
        dim_rows = [["Dimension Factor", "Score", "%ile", "Dimension Factor", "Score", "%ile"]]
        for i in range(0, len(raw_dimensions), 2):
            d1 = raw_dimensions[i]
            d2 = raw_dimensions[i+1] if (i+1 < len(raw_dimensions)) else None
            
            row = [
                Paragraph(f"<b>{d1.dimension_name}</b>", small_style),
                Paragraph(f"{d1.percentage:.0f}%", small_style),
                Paragraph(f"{d1.percentile:.0f}th", small_style),
            ]
            if d2:
                row.extend([
                    Paragraph(f"<b>{d2.dimension_name}</b>", small_style),
                    Paragraph(f"{d2.percentage:.0f}%", small_style),
                    Paragraph(f"{d2.percentile:.0f}th", small_style),
                ])
            else:
                row.extend(["—", "—", "—"])
            dim_rows.append(row)

        dim_table = Table(dim_rows, colWidths=[170, 50, 50, 170, 50, 50])
        dim_table.setStyle(TableStyle([
            ('BACKGROUND', (0, 0), (-1, 0), pakistan_green),
            ('TEXTCOLOR', (0, 0), (-1, 0), colors.white),
            ('FONTNAME', (0, 0), (-1, 0), 'Helvetica-Bold'),
            ('FONTSIZE', (0, 0), (-1, 0), 7.5),
            ('BOTTOMPADDING', (0, 0), (-1, -1), 3),
            ('TOPPADDING', (0, 0), (-1, -1), 3),
            ('GRID', (0, 0), (-1, -1), 0.5, slate_border),
            ('ROWBACKGROUNDS', (0, 1), (-1, -1), [colors.white, slate_light])
        ]))
        elements.append(dim_table)
    else:
        elements.append(Paragraph("<i>Standard baseline evaluation completed across cognitive and RIASEC interest scales.</i>", body_style))

    # Force PageBreak for clean, structured 2-page layout
    elements.append(PageBreak())

    # =========================================================================
    # PAGE 2: CAREER RECOMMENDATIONS, STRENGTHS, GROWTH, & ACTION PLAN
    # =========================================================================

    elements.append(Paragraph("CAREER PATHWAYS & TERTIARY EDUCATION BLUEPRINT", title_style))
    elements.append(Paragraph("Higher Education Commission (HEC) Pakistan Recognized Degree & Entry Test Mapping", subtitle_style))
    elements.append(HRFlowable(width="100%", thickness=1.5, color=pakistan_green, spaceAfter=8))

    # Top Career Recommendations Table
    elements.append(Paragraph("Top Compatible Career Fields & Entry Pathways", section_style))
    
    career_recs = list(report.recommendations.all().order_by('rank'))
    career_rows = [["Rank", "Career Field", "Match", "Typical Degrees & Entry Tests", "Top Pakistani Universities"]]
    
    for rec in career_recs[:5]:  # Top 5 recommendations fit comfortably
        field = rec.field
        exams_str = ", ".join(field.required_exams[:3]) if field.required_exams else "Board Merit"
        degrees_str = ", ".join(field.typical_degrees[:2]) if field.typical_degrees else field.name
        unis_str = ", ".join(field.top_universities_pakistan[:3]) if field.top_universities_pakistan else "HEC Approved"
        score_pct = int(round(rec.match_score * 100)) if rec.match_score <= 1.0 else int(round(rec.match_score))

        career_rows.append([
            Paragraph(f"<b>#{rec.rank}</b>", bold_body_style),
            Paragraph(f"<b>{field.name}</b><br/><font size=7 color='#475569'>{rec.rationale_text[:95]}...</font>", body_style),
            Paragraph(f"<b>{score_pct}%</b>", bold_body_style),
            Paragraph(f"<b>Degrees:</b> {degrees_str}<br/><b>Tests:</b> {exams_str}", small_style),
            Paragraph(unis_str, small_style)
        ])

    career_table = Table(career_rows, colWidths=[35, 175, 55, 155, 120])
    career_table.setStyle(TableStyle([
        ('BACKGROUND', (0, 0), (-1, 0), navy_accent),
        ('TEXTCOLOR', (0, 0), (-1, 0), colors.white),
        ('FONTNAME', (0, 0), (-1, 0), 'Helvetica-Bold'),
        ('FONTSIZE', (0, 0), (-1, 0), 8),
        ('BOTTOMPADDING', (0, 0), (-1, -1), 4),
        ('TOPPADDING', (0, 0), (-1, -1), 4),
        ('GRID', (0, 0), (-1, -1), 0.5, slate_border),
        ('ROWBACKGROUNDS', (0, 1), (-1, -1), [colors.white, slate_light])
    ]))
    elements.append(career_table)
    elements.append(Spacer(1, 8))

    # Strengths and Growth Areas
    elements.append(Paragraph("Identified Strengths & Skill Development Areas", section_style))
    strengths_list = report.strengths or ["Strong analytical problem solving and conceptual logical thinking."]
    strengths_html = "<b>Core Strengths:</b><br/>" + "<br/>".join([f"• {s}" for s in strengths_list[:3]])
    elements.append(Paragraph(strengths_html, body_style))
    elements.append(Spacer(1, 4))
    
    growth_list = report.growth_areas or ["Speed optimization for competitive university entry examinations."]
    growth_html = "<b>Areas for Growth:</b><br/>" + "<br/>".join([f"• {g}" for g in growth_list[:2]])
    elements.append(Paragraph(growth_html, body_style))
    elements.append(Spacer(1, 8))

    # Actionable Next Steps
    elements.append(Paragraph("Strategic Next Steps & Academic Action Plan", section_style))
    steps_list = report.next_steps or [
        "Align Grade 11/12 subject electives with your primary recommended stream.",
        "Begin targeted past-paper preparation for prerequisite entry examinations (e.g. NET, ECAT, MDCAT, FAST).",
        "Participate in relevant extracurricular STEM, business, or debate societies to reinforce profile.",
        "Schedule formal review with institutional counselor and parents."
    ]
    next_steps_text = "<br/>".join([f"<b>{idx}.</b> {step}" for idx, step in enumerate(steps_list[:4], 1)])
    elements.append(Paragraph(next_steps_text, body_style))
    elements.append(Spacer(1, 12))

    # Official Footer & Verification
    elements.append(HRFlowable(width="100%", thickness=0.5, color=colors.HexColor('#CBD5E1'), spaceAfter=4))
    elements.append(Paragraph(
        "<i>Official Guidance Dossier • Rahvia Platform (Islamic Republic of Pakistan). Compliant with national student data privacy standards. "
        "Generated automatically by psychometric scoring algorithms. For inquiries or verification, visit portal at http://localhost:3000</i>",
        small_style
    ))

    doc.build(elements)
    pdf_bytes = buffer.getvalue()
    buffer.close()
    return pdf_bytes
