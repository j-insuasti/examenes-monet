from django.test import TestCase
from .models import Student

class StudentModelTest(TestCase):
    def setUp(self):
        Student.objects.create(name="Jhon", email="jhon@ejemplo.com", registration_number="1234")

    def test_student_has_name(self):
        student = Student.objects.get(id=1)
        self.assertEqual(student.name, "Jhon")
