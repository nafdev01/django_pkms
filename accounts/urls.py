# accounts/urls.py
from django.urls import path, include
from .views import *
from django.contrib.auth import urls as auth_urls


urlpatterns = [
    # standard auth urls
    path("login/", login, name="login"),
    path("signup/", register, name="signup"),
    # profile urls
    path("profile/edit/", edit_profile, name="edit_profile"),
    path("profile/", profile, name="profile"),
    path("profile/<int:user_id>/<username>/", profile, name="profile"),
    path("delete/", delete_account, name="delete_account"),
    path("", include(auth_urls)),
]
