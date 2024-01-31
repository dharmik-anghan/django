from django.urls import path
from account.views import (
    UserRegistrationView,
    UserLoginView,
    UserProfileView,
    UserChangePasswordView,
    SentResetPasswordEmailView,
    UserPasswordResetView,
)

urlpatterns = [
    path("register/", UserRegistrationView.as_view(), name="register"),
    path("login/", UserLoginView.as_view(), name="login"),
    path("profile/", UserProfileView.as_view(), name="profile"),
    path("resetpassword/", UserChangePasswordView.as_view(), name="resetpassword"),
    path(
        "sent-reset-password-email/",
        SentResetPasswordEmailView.as_view(),
        name="sent-reset-password-email",
    ),
    path(
        "reset-password/<uid>/<token>/",
        UserPasswordResetView.as_view(),
        name="reset-password",
    ),
]
