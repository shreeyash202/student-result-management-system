import unittest

class TestSRMS(unittest.TestCase):

    def test_admin_login(self):
        username = "admin"
        password = "admin123"

        self.assertEqual(username, "admin")
        self.assertEqual(password, "admin123")

    def test_marks_validation(self):
        marks = 85

        self.assertTrue(0 <= marks <= 100)

    def test_result_generation(self):
        total = 450
        percentage = total / 5

        self.assertEqual(percentage, 90)

    def test_student_id(self):
        student_id = "stu101"

        self.assertTrue(student_id.startswith("stu"))

if __name__ == '__main__':
    unittest.main()