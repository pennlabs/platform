from unittest.mock import patch

from django.test import TestCase

from accounts.models import Major
from accounts.update_majors import update_majors


@patch("accounts.update_majors.requests.get")
class UpdateMajorsTestCase(TestCase):

    def testTotalMajorCount(self, mock_source_file):
        with open(r"PennCoursePrograms.html", "r") as f:
            mock_source_file.return_value.text = f.read()

        update_majors()

        self.assertEquals(Major.objects.all().count(), 469)

    def testBachelorMajorCount(self, mock_source_file):
        with open(r"PennCoursePrograms.html", "r") as f:
            mock_source_file.return_value.text = f.read()

        update_majors()

        self.assertEquals(Major.objects.filter(degree_type="BACHELORS").count(), 215)

    def testMasterCount(self, mock_source_file):
        with open(r"PennCoursePrograms.html", "r") as f:
            mock_source_file.return_value.text = f.read()

        update_majors()

        self.assertEquals(Major.objects.filter(degree_type="MASTERS").count(), 123)

    def testProfessionalCount(self, mock_source_file):
        with open(r"PennCoursePrograms.html", "r") as f:
            mock_source_file.return_value.text = f.read()

        update_majors()

        self.assertEquals(Major.objects.filter(degree_type="PROFESSIONAL").count(), 47)
