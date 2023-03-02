import pyotp
import qrcode
from accounts.models import *


def generate_2fa(user):
    student = Student.objects.get(id=user.id)
    
    # Generate a secret key
    secret = pyotp.random_base32()
    
    two_factor = TwoFactorAuth.objects.get_or_create(student=student)
    


    # Print the QR code URL
    totp = pyotp.TOTP(secret)
    uri = totp.provisioning_uri(name=student.get_username(), issuer_name="issuer")
    img = qrcode.make(uri)

    # Save the QR code as an image
    img.save("qrcode.png")
