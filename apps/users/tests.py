from django.test import TestCase, Client
from django.urls import reverse
from apps.users.models import CustomUser
from django.core.files.uploadedfile import SimpleUploadedFile


class UserModelTests(TestCase):
    def setUp(self):
        self.user = CustomUser.objects.create_user(
            username="testuser",
            password="securepassword123",
            email="test@example.com",
            phone_number="1234567890",
            date_of_birth="2000-01-01",
        )

    def test_user_str(self):
        self.assertEqual(str(self.user), "testuser")

    def test_profile_completion(self):
        self.assertEqual(self.user.calculate_completion(), 100)  # 3 out of 3 fields filled


class UserViewsTests(TestCase):
    def setUp(self):
        self.client = Client()
        self.password = "strongpass456"
        self.user = CustomUser.objects.create_user(
            username="john",
            password=self.password,
            email="john@example.com"
        )

    def test_signup_view_get(self):
        response = self.client.get(reverse("signup"))
        self.assertEqual(response.status_code, 200)

    def test_signup_view_post(self):
        response = self.client.post(reverse("signup"), {
            "username": "newuser",
            "first_name": "New",
            "last_name": "User",
            "email": "newuser@example.com",
            "password1": "testpassword123",
            "password2": "testpassword123"
        })
        self.assertRedirects(response, reverse("registration_success"))
        self.assertTrue(CustomUser.objects.filter(username="newuser").exists())

    def test_login_view_success(self):
        response = self.client.post(reverse("login"), {
            "username": "john",
            "password": self.password
        })
        self.assertRedirects(response, reverse("home"))

    def test_login_view_failure(self):
        response = self.client.post(reverse("login"), {
            "username": "john",
            "password": "wrongpass"
        })
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, "Invalid username or password")

    def test_dashboard_view_authenticated(self):
        self.client.login(username="john", password=self.password)
        response = self.client.get(reverse("dashboard"))
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, "john")

    def test_edit_profile_view_get(self):
        self.client.login(username="john", password=self.password)
        response = self.client.get(reverse("edit_profile"))
        self.assertEqual(response.status_code, 200)

    def test_edit_profile_view_post(self):
        self.client.login(username="john", password=self.password)
        response = self.client.post(reverse("edit_profile"), {
            "email": "newjohn@example.com",
            "phone_number": "9876543210",
            "date_of_birth": "1995-05-10"
        })
        self.assertRedirects(response, reverse("dashboard"))
        self.user.refresh_from_db()
        self.assertEqual(self.user.email, "newjohn@example.com")

    def test_logout_view(self):
        self.client.login(username="john", password=self.password)
        response = self.client.post(reverse("logout"))
        self.assertRedirects(response, reverse("home"))
