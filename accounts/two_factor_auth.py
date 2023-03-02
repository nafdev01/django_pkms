import os
import pyotp
import qrcode
from django.conf import settings
from accounts.models import *


def student_directory_path(instance, filename):
    # file will be uploaded to MEDIA_ROOT/user_<id>/<filename>
    return f"user_{instance.student.username}/profile_photo/{filename}"


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
    two_factor.two_factor_status = "EN"


def authenticate_2fa(user):
    student = Student.objects.get(id=user.id)
    two_factor = TwoFactorAuth.objects.get(student=student)

    # Load the secret key from the students two factor profile
    secret = two_factor.two_factor_secret

    # Verify the OTP
    totp = pyotp.TOTP(secret)
    otp = input("Enter 6-digit code from Google Authenticator: ")
    if totp.verify(otp):
        print("OTP is valid")
    else:
        print("OTP is invalid")
