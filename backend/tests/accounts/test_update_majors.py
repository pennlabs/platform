from unittest.mock import patch

from django.test import TestCase

from accounts.models import Major
from accounts.update_majors import update_all_majors


@patch("accounts.update_majors.requests.get")
class UpdateMajorsTestCase(TestCase):
    def setUp(self):
        with open(r"./tests/accounts/PennCoursePrograms.html", "r") as f:
            self.html = f.read()

    def testTotalMajorCount(self, mock_source_file):
        mock_source_file.return_value.text = self.html
        update_all_majors()

        self.assertEqual(Major.objects.all().count(), 469)

    def testBachelorMajorCount(self, mock_source_file):
        mock_source_file.return_value.text = self.html
        update_all_majors()

        self.assertEqual(Major.objects.filter(degree_type="BACHELORS").count(), 215)

    def testMasterCount(self, mock_source_file):
        mock_source_file.return_value.text = self.html
        update_all_majors()

        self.assertEqual(Major.objects.filter(degree_type="MASTERS").count(), 123)

    def testProfessionalCount(self, mock_source_file):
        mock_source_file.return_value.text = self.html
        update_all_majors()

        self.assertEqual(Major.objects.filter(degree_type="PROFESSIONAL").count(), 47)
