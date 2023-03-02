# import pyotp
# import qrcode
# from accounts.models import *


# def generate_2fa(student):
#     # Generate a secret key
#     secret = pyotp.random_base32()

#     # Save the secret key to a file
#     with open("secretmine.txt", "w") as f:
#         f.write(secret)

#     # Print the QR code URL
#     totp = pyotp.TOTP(secret)
#     uri = totp.provisioning_uri(name=student.get_username(), issuer_name=student.)
#     img = qrcode.make(uri)

#     # Save the QR code as an image
#     img.save("qrcode.png")
