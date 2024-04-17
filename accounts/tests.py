from django.test import TestCase
from accounts.models import UserProfile
from django.contrib.auth.models import User

# Create your tests here.

class UserProfileTestCase(TestCase):
    def setUp(self):
        self.user = User.objects.create(username="bob", password="1234")
        self.user2 = User.objects.create(username="Rob", password="5432")
        UserProfile.objects.create(self.user)
        UserProfile.objects.create(self.user2)

    def test_role(self):
        userprofile = UserProfile.objects.get(user=self.user)
        userprofile2 = UserProfile.objects.get(user=self.user2)
        self.assertEqual(userprofile.role, "student")
        self.assertEqual(userprofile2.role, "student")
