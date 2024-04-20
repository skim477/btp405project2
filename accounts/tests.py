from django.test import TestCase, Client, RequestFactory
from accounts.models import UserProfile
from django.contrib.auth.models import User
from django.urls import reverse, reverse_lazy
from accounts.form import SignUpForm  # Import SignUpForm
from accounts.views import SignUpView, CustomLoginView
from unittest.mock import patch

# Create your tests here.

class UserProfileTestCase(TestCase):
    def setUp(self):
        self.user = User.objects.create(username="bob", password="1234")
        self.user2 = User.objects.create(username="Rob", password="5432")
        UserProfile.objects.create(user=self.user)
        UserProfile.objects.create(user=self.user2)

    def test_role(self):
        userprofile = UserProfile.objects.get(user=self.user)
        userprofile2 = UserProfile.objects.get(user=self.user2)
        self.assertEqual(userprofile.role, "student")
        self.assertEqual(userprofile2.role, "student")

class SignUpViewTest(TestCase):
    def setUp(self):
        self.client = Client()
        self.signup_url = reverse('signup')

    def test_signup_form_valid(self):
        # Create a form data dictionary with valid data
        form_data = {
            'username': 'testuser',
            'password1': 'testpassword',
            'password2': 'testpassword',
            'first_name': 'test',
            'last_name': 'tester',
            'email': 'adielroytgarts@gmail.com',
            'role': 'teacher'
            # Add other required fields as necessary
        }

        # Submit the form data
        response = self.client.post(self.signup_url, form_data, follow=True)

        self.assertEqual(response.status_code, 200)
        

        # Check that the form submission redirects to the login page
        #self.assertEqual(response.url, reverse('login'))  # Redirect URL

        # Check that the user was created
        self.assertTrue(User.objects.filter(username='testuser').exists())

        # Optionally, you can check for the user's role and redirection behavior here

    @patch('accounts.views.login')
    def test_signup_form_valid_with_role_redirect(self, mock_login):
        # Create a user profile with a specific role

        # Create a form data dictionary with valid data
        form_data = {
            'username': 'testuser2',
            'first_name': 'test',
            'last_name': 'tester',
            'email': 'adielroytgarts@gmail.com',
            'password1': 'testpassword',
            'password2': 'testpassword',
            'role': 'teacher'
            # Add other required fields as necessary
        }

        # Submit the form data
        response = self.client.post(self.signup_url, form_data, follow=True)


        # Check that the response redirects to the index page
        self.assertEqual(response.status_code, 200)
        #self.assertEqual(response.url, reverse('index'))

class CustomLoginViewTest(TestCase):
    def setUp(self):
        self.factory = RequestFactory()

    def test_get_success_url_teacher(self):
        # Create a user with the role 'teacher'
        user = User.objects.create_user(username='teacher', password='password')
        UserProfile.objects.create(user=user, role='teacher')

        # Create a request object
        request = self.factory.get('/')

        # Set the user for the request
        request.user = user

        # Instantiate CustomLoginView
        view = CustomLoginView()

        # Set the request for the view
        view.request = request

        # Call the get_success_url method
        success_url = view.get_success_url()

        # Check that the returned URL is 'index'
        self.assertEqual(success_url, reverse_lazy('index'))

    def test_get_success_url_student(self):
        # Create a user with the role 'student'
        user = User.objects.create_user(username='student', password='password')
        UserProfile.objects.create(user=user, role='student')

        # Create a request object
        request = self.factory.get('/')

        # Set the user for the request
        request.user = user

        # Instantiate CustomLoginView
        view = CustomLoginView()

        # Set the request for the view
        view.request = request

        # Call the get_success_url method
        success_url = view.get_success_url()

        # Check that the returned URL is 'profile' with the user's ID as a parameter
        expected_url = reverse_lazy('profile', kwargs={'id': user.id})
        self.assertEqual(success_url, expected_url)

    def test_get_success_url_default(self):
        # Create a user with no associated profile
        user = User.objects.create_user(username='default_user', password='password')

        # Create a request object
        request = self.factory.get('/')

        # Set the user for the request
        request.user = user

        # Instantiate CustomLoginView
        view = CustomLoginView()

        # Set the request for the view
        view.request = request

        # Call the get_success_url method
        success_url = view.get_success_url()

        # Check that the returned URL is the default success URL
        self.assertEqual(success_url, reverse_lazy('index'))