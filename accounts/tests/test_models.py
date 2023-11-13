from rest_framework.test import APITestCase
from ..models import User


class TestModels(APITestCase):
    def test_creates_user(self):
        user = User.objects.create_user(
            username='user', 
            email='user@email.com', 
            password='userpassword', 
            date_of_birth='2000-01-01'
        )
        self.assertIsInstance(user, User)
        self.assertEqual(user.email, 'user@email.com')
        self.assertFalse(user.is_superuser)


    def test_raises_error_with_message_when_email_is_not_supplied(self):
        with self.assertRaisesMessage(ValueError, "The email is required"):
            User.objects.create_user(
                username='user', 
                email='', 
                password='userpassword', 
                date_of_birth='2000-01-01'
            )


    def test_creates_super_user(self):
        user = User.objects.create_superuser(
            username='user', 
            email='user@email.com', 
            password='userpassword', 
            date_of_birth='2000-01-01'
        )
        self.assertIsInstance(user, User)
        self.assertEqual(user.email, 'user@email.com')
        self.assertTrue(user.is_superuser)

    
    def test_raises_error_with_message_when_super_user_is_not_staff(self):
        with self.assertRaisesMessage(ValueError, "SuperUser must have is_staff=True"):
            User.objects.create_superuser(
                username='user', 
                email='user@email.com', 
                password='userpassword', 
                date_of_birth='2000-01-01',
                is_staff=False
            )


    def test_raises_error_with_message_when_super_user_is_not_superuser(self):
        with self.assertRaisesMessage(ValueError, "SuperUser must have is_superuser=True"):
            User.objects.create_superuser(
                username='user', 
                email='user@email.com', 
                password='userpassword', 
                date_of_birth='2000-01-01',
                is_superuser=False
            )