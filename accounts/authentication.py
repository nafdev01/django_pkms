# accounts/authentication.py
import os
import shutil
import pyotp
import qrcode
from django.conf import settings
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


def generate_2fa(user):
    student = Student.objects.get(id=user.id)
    two_factor, created = TwoFactorAuth.objects.get_or_create(student=student)
    secret = two_factor.two_factor_secret

    # Print the QR code URL
    totp = pyotp.TOTP(secret)
    uri = totp.provisioning_uri(
        name=student.twofactorauth.two_factor_name,
        issuer_name=student.twofactorauth.two_factor_issuer,
    )
    img = qrcode.make(uri)

    # Define the directory path
    directory_path = os.path.join(
        settings.MEDIA_ROOT, f"user_{student.get_username()}/2fa"
    )

    # Check if directory exists
    if not os.path.exists(directory_path):
        # Create the directory if it doesn't exist
        os.makedirs(directory_path)

    # Define the file path
    file_path = os.path.join(directory_path, "qr_code.png")

    # Save the QR code as an image
    img.save(file_path)

    # set the two_factor_status to enabled
    two_factor.two_factor_status = TwoFactorAuth.TwoFactorStatus.ENABLED
    two_factor.save()


# def authenticate_2fa(user, otp):
#     student = Student.objects.get(id=user.id)
#     two_factor = TwoFactorAuth.objects.get(student=student)

#     # Load the secret key from the student's two-factor profile
#     secret = two_factor.two_factor_secret

#     if two_factor.two_factor_status != TwoFactorAuth.TwoFactorStatus.ACTIVATED:
#         two_factor.two_factor_status = TwoFactorAuth.TwoFactorStatus.ACTIVATED
#         two_factor.save()

#     # Verify the OTP
#     totp = pyotp.TOTP(secret)
#     if not totp.verify(otp):
#         return False
#     else:
#         # Authentication successful. Delete the 2FA folder if it exists
#         directory_path = os.path.join(
#             settings.MEDIA_ROOT, f"user_{student.get_username()}/2fa"
#         )
#         if os.path.exists(directory_path):
#             shutil.rmtree(directory_path)

#         return True
