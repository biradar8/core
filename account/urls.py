from django.urls import path

from account.views import (
    AccountLoginView,
    RegistrationView,
    AccountProfileView,
    AccountChangePasswordView,
    AccountResetPasswordEmailView,
    AccountResetPasswordView,
)

urlpatterns = [
    path("register/", RegistrationView.as_view(), name="register"),
    path("login/", AccountLoginView.as_view(), name="login"),
    path("profile/", AccountProfileView.as_view(), name="profile"),
    path("changepassword/", AccountChangePasswordView.as_view(), name="changepassword"),
    path("resetpassword-mail/", AccountResetPasswordEmailView.as_view(), name="resetpassword_mail"),
    path("resetpassword/<uid>/<token>/", AccountResetPasswordView.as_view(), name="resetpassword"),
]
