from django.test import TestCase
from rest_framework.test import APIClient
from rest_framework import status
from authentication.models import User
from schools.models import School

class SchoolCounselorPrivacyTests(TestCase):
    def setUp(self):
        self.client = APIClient()

        # Create two distinct schools
        self.school_a = School.objects.create(
            name="Government National College",
            code="GNC-01",
            city="Karachi",
            board=School.BoardChoice.BISE_KARACHI
        )
        self.school_b = School.objects.create(
            name="Islamabad Model College",
            code="IMC-01",
            city="Islamabad",
            board=School.BoardChoice.FBISE_ISLAMABAD
        )

        # Create counselor assigned to School A
        self.counselor_a = User.objects.create_user(
            email="counselor.a@school.pk",
            password="Password123!",
            role=User.Role.COUNSELOR
        )
        self.school_a.counselor = self.counselor_a
        self.school_a.save()

        # Create counselor assigned to School B
        self.counselor_b = User.objects.create_user(
            email="counselor.b@school.pk",
            password="Password123!",
            role=User.Role.COUNSELOR
        )
        self.school_b.counselor = self.counselor_b
        self.school_b.save()

    def test_counselor_only_sees_own_school_in_list(self):
        """Authenticated counselor only sees their own assigned institution"""
        self.client.force_authenticate(user=self.counselor_a)
        res = self.client.get("/api/schools/")
        self.assertEqual(res.status_code, status.HTTP_200_OK)
        results = res.data.get('results', res.data)
        school_codes = [s["code"] for s in results]
        self.assertEqual(school_codes, ["GNC-01"])
        self.assertNotIn("IMC-01", school_codes)

    def test_counselor_cannot_access_other_school_dashboard(self):
        """Counselor A is forbidden (403) from inspecting School B cohort dashboard"""
        self.client.force_authenticate(user=self.counselor_a)
        res = self.client.get(f"/api/school/{self.school_b.school_id}/dashboard")
        self.assertEqual(res.status_code, status.HTTP_403_FORBIDDEN)

    def test_counselor_can_access_own_school_dashboard(self):
        """Counselor A can successfully access School A dashboard"""
        self.client.force_authenticate(user=self.counselor_a)
        res = self.client.get(f"/api/school/{self.school_a.school_id}/dashboard")
        self.assertEqual(res.status_code, status.HTTP_200_OK)
        self.assertEqual(res.data["school"]["code"], "GNC-01")
