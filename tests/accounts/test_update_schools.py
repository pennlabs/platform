from unittest.mock import patch

from django.test import TestCase

from accounts.models import School
from accounts.update_schools import update_all_schools


@patch("accounts.update_schools.requests.get")
class UpdateMajorsTestCase(TestCase):
    def testTotalSchoolCount(self, mock_source_file):
        with open(r"PennCoursePrograms.html", "r") as f:
            mock_source_file.return_value.text = f.read()

        update_all_schools()

        self.assertEquals(School.objects.all().count(), 12)
