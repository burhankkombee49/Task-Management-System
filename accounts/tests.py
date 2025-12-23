from django.test import TestCase
from django.contrib.auth import get_user_model

User = get_user_model()

class UserModelTest(TestCase):

    def test_user_is_created(self):
        user = User.objects.create_user(
            username="testuser",
            email="test@test.com",
            password="test123"
        )

        self.assertEqual(user.username, "testuser")
        self.assertEqual(user.email, "test@test.com")
