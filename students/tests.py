from django.test import TestCase
from django.contrib.auth.models import User
from students.models import Student

class StudentModelTest(TestCase):
    def setUp(self):
        # Create a user for the student
        self.user = User.objects.create(username='testuser', email='test@example.com')
        
        # Create a student object
        self.student = Student.objects.create(
            user=self.user,
            student_number=123456,
            first_name='John',
            last_name='Doe',
            email='john.doe@example.com',
            field_of_study='Computer Science',
            gpa=3.8
        )

    def test_student_str_method(self):
        # Test the __str__ method of the Student model
        expected_str = f'STUDENT: {self.student.first_name} {self.student.last_name}'
        self.assertEqual(str(self.student), expected_str)

    def test_student_attributes(self):
        # Test attributes of the student object
        self.assertEqual(self.student.user, self.user)
        self.assertEqual(self.student.student_number, 123456)
        self.assertEqual(self.student.first_name, 'John')
        self.assertEqual(self.student.last_name, 'Doe')
        self.assertEqual(self.student.email, 'john.doe@example.com')
        self.assertEqual(self.student.field_of_study, 'Computer Science')
        self.assertEqual(self.student.gpa, 3.8)