# accounts/urls.py
from django.urls import path, include
from .views import *
from django.contrib.auth import urls as auth_urls


urlpatterns = [
    path("login/", UserLoginView.as_view(), name="login"),
    path("signup/", register, name="signup"),
    path("profile/edit/", edit_profile, name="edit_profile"),
    path("profile/", profile, name="profile"),
    path("profile/<int:user_id>/<username>/", profile, name="profile"),
    path("", include(auth_urls)),
]
