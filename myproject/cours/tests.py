from django.test import TestCase
from .models import Course



class CourseTests(TestCase):

    def setUp(self):
        self.course = Course.objects.create(
            name="Python Basics",
            instructor="John Doe",
            category="Programming",
            schedule="Mon-Wed 10:00 - 12:00"
        )

    def test_course_creation(self):
        self.assertEqual(Course.objects.count(), 1)
        self.assertEqual(self.course.name, "Python Basics")
        self.assertEqual(self.course.instructor, "John Doe")

    def test_course_retrieval(self):
        course = Course.objects.get(course_id=self.course.course_id)
        self.assertIsNotNone(course)
        self.assertEqual(course.category, "Programming")

    def test_course_update(self):
        self.course.name = "Advanced Python"
        self.course.save()

        updated_course = Course.objects.get(course_id=self.course.course_id)
        self.assertEqual(updated_course.name, "Advanced Python")

    def test_course_deletion(self):
        self.course.delete()
        self.assertEqual(Course.objects.count(), 0)
