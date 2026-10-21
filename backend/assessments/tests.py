from django.test import TestCase
from django.urls import reverse
from rest_framework.test import APIClient
from rest_framework import status
from authentication.models import User
from schools.models import School
from students.models import Student
from careers.models import CareerField
from assessments.models import Question, AssessmentSession
from recommendations.models import Report

class RahviaPlatformCoreTests(TestCase):
    def setUp(self):
        self.client = APIClient()

        # Create School
        self.school = School.objects.create(
            name="Islamabad Model College",
            code="IMC-TEST",
            board=School.BoardChoice.FBISE_ISLAMABAD,
            city="Islamabad",
            contact_email="imc@test.edu.pk"
        )

        # Create Student User
        self.student_user = User.objects.create_user(
            email="teststudent@rahvia.pk",
            password="TestPassword123!",
            first_name="Bilal",
            last_name="Ahmed",
            role=User.Role.STUDENT,
            parent_consent_granted=True
        )
        self.student = Student.objects.create(
            user=self.student_user,
            school=self.school,
            name="Bilal Ahmed",
            board="FBISE Islamabad",
            current_grade=Student.GradeChoice.MATRIC_10TH,
            elective_group=Student.ElectiveGroupChoice.SCIENCE_CS,
            academic_scores={"Math": 85, "Physics": 90, "Computer": 92},
            interests=["Coding", "AI", "Robotics"],
            parent_consent=True
        )

        # Create Counselor User
        self.counselor_user = User.objects.create_user(
            email="testcounselor@rahvia.pk",
            password="TestPassword123!",
            role=User.Role.COUNSELOR
        )
        self.school.counselor = self.counselor_user
        self.school.save()

        # Create Career Field
        self.career_cs = CareerField.objects.create(
            name="Software Engineering & AI",
            category=CareerField.CategoryChoice.COMPUTING_AI,
            stream_requirement=CareerField.StreamChoice.ICS,
            description="Software and AI systems development.",
            typical_degrees=["BS Software Engineering", "BS CS"],
            required_exams=["FAST", "NET"],
            top_universities_pakistan=["FAST-NU", "NUST"]
        )

        # Create Question Bank Items
        self.q_math = Question.objects.create(
            text="What is 15 * 12?",
            type=Question.TypeChoice.MCQ,
            category=Question.CategoryChoice.APTITUDE,
            dimension="NumericalAptitude",
            correct_answer="A",
            correct_answer_weight=1.0,
            options=[{"id": "A", "text": "180"}, {"id": "B", "text": "150"}]
        )
        self.q_likert = Question.objects.create(
            text="I enjoy writing computer code.",
            type=Question.TypeChoice.LIKERT,
            category=Question.CategoryChoice.INTEREST,
            dimension="RIASEC_Investigative",
            options=[
                {"id": "1", "text": "1", "score": 1.0},
                {"id": "5", "text": "5", "score": 5.0}
            ]
        )

    def test_01_user_authentication(self):
        """Test registration and JWT login"""
        # Register
        reg_payload = {
            "email": "newstudent@rahvia.pk",
            "password": "StrongPassword2026!",
            "name": "Fatima Zahra",
            "role": "STUDENT",
            "parent_guardian_name": "Zahra Bibi",
            "parent_guardian_email": "zahra@example.com",
            "parent_consent_granted": True
        }
        res_reg = self.client.post("/api/auth/register", reg_payload, format="json")
        self.assertEqual(res_reg.status_code, status.HTTP_201_CREATED)
        self.assertIn("tokens", res_reg.data)

        # Login
        login_payload = {
            "email": "newstudent@rahvia.pk",
            "password": "StrongPassword2026!"
        }
        res_login = self.client.post("/api/auth/login", login_payload, format="json")
        self.assertEqual(res_login.status_code, status.HTTP_200_OK)
        self.assertIn("access", res_login.data["tokens"])

    def test_02_assessment_workflow_and_scoring(self):
        """Test start, question fetch, submit, score computation, and report generation"""
        self.client.force_authenticate(user=self.student_user)

        # Start assessment
        res_start = self.client.post("/api/assessment/start", {}, format="json")
        self.assertEqual(res_start.status_code, status.HTTP_201_CREATED)
        assessment_id = res_start.data["assessment_id"]

        # Get questions
        res_q = self.client.get(f"/api/assessment/{assessment_id}/questions")
        self.assertEqual(res_q.status_code, status.HTTP_200_OK)
        self.assertGreaterEqual(res_q.data["total_questions"], 2)

        # Submit answers
        submit_payload = {
            "time_spent_seconds": 180,
            "answers": [
                {"question_id": str(self.q_math.question_id), "student_answer": "A", "time_taken_seconds": 45},
                {"question_id": str(self.q_likert.question_id), "student_answer": "5", "time_taken_seconds": 25}
            ]
        }
        res_sub = self.client.post(f"/api/assessment/{assessment_id}/submit", submit_payload, format="json")
        self.assertEqual(res_sub.status_code, status.HTTP_200_OK)
        self.assertIn("report_id", res_sub.data)
        report_id = res_sub.data["report_id"]

        # Fetch Report by Student
        res_rep = self.client.get(f"/api/report/{self.student.student_id}")
        self.assertEqual(res_rep.status_code, status.HTTP_200_OK)
        self.assertTrue(len(res_rep.data["recommended_streams"]) > 0)
        self.assertTrue(len(res_rep.data["recommendations"]) > 0)

        # Download PDF Report
        res_pdf = self.client.get(f"/api/report/{report_id}/pdf")
        self.assertEqual(res_pdf.status_code, status.HTTP_200_OK)
        self.assertEqual(res_pdf["Content-Type"], "application/pdf")
        self.assertGreater(len(res_pdf.content), 500)

    def test_03_school_counselor_dashboard(self):
        """Test school aggregate statistics and student roster"""
        self.client.force_authenticate(user=self.counselor_user)
        res = self.client.get(f"/api/school/{self.school.school_id}/dashboard")
        self.assertEqual(res.status_code, status.HTTP_200_OK)
        self.assertIn("summary", res.data)
        self.assertIn("roster", res.data)
        self.assertEqual(res.data["summary"]["total_students"], 1)

    def test_04_admin_question_endpoint_security(self):
        """Test that unauthenticated requests to /api/admin/questions are rejected with 401"""
        res_unauth = self.client.get("/api/admin/questions")
        self.assertEqual(res_unauth.status_code, status.HTTP_401_UNAUTHORIZED)

        # Student user should also be forbidden
        self.client.force_authenticate(user=self.student_user)
        res_student = self.client.get("/api/admin/questions")
        self.assertEqual(res_student.status_code, status.HTTP_403_FORBIDDEN)

    def test_05_health_check_endpoint(self):
        """Test system health check endpoint"""
        res = self.client.get("/api/health")
        self.assertEqual(res.status_code, status.HTTP_200_OK)
        data = res.json()
        self.assertEqual(data["status"], "healthy")
        self.assertEqual(data["database"], "connected")

    def test_06_career_fields_public_listing(self):
        """Test public career fields encyclopedia endpoint"""
        res = self.client.get("/api/careers/")
        self.assertEqual(res.status_code, status.HTTP_200_OK)
        self.assertGreaterEqual(len(res.data), 1)
