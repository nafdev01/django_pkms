# accounts/authentication.py
from accounts.models import *
from accounts.models import *


class EmailAuthenticationBackend:
    # authenticate user using email address
    def authenticate(self, request, username=None, password=None):
        try:
            user = Student.objects.get(email=username)
            if user.check_password(password):
                return user
            return None
        except (Student.DoesNotExist, Student.MultipleObjectsReturned):
            return None

    def get_user(self, user_id):
        try:
            return Student.objects.get(pk=user_id)
        except Student.DoesNotExist:
            return None

    def create_profile(backend, user, *args, **kwargs):
        """
        Create user profile for social authentication
        """
        Profile.objects.get_or_create(user=user)
