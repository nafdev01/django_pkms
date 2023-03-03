# accounts/urls.py
from django.urls import path, include
from .views import *
from django.contrib.auth import urls as auth_urls


urlpatterns = [
    # standard auth urls
    path("login/", login, name="login"),
    path("signup/", register, name="signup"),
    # two factor authentication urls
    path("2fa-qr-code/", display_qrcode, name="display_qrcode"),
    path("2fa/verify/", verify_2fa, name="verify_2fa"),
    # profile urls
    path("profile/edit/", edit_profile, name="edit_profile"),
    path("profile/", profile, name="profile"),
    path("profile/<int:user_id>/<username>/", profile, name="profile"),
    path("", include(auth_urls)),
]
