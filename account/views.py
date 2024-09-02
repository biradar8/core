from django.contrib.auth import authenticate
from rest_framework import status
from rest_framework.permissions import AllowAny, IsAuthenticated
from rest_framework.response import Response
from rest_framework.views import APIView

from account.renderers import AccountRenderer
from account.serializers import (
    AccountSerializer,
    AccountLoginSerializer,
    AccountProfileSerializer,
    AccountChangePasswordSerializer,
    AccountResetPasswordEmailSerializer,
    AccountResetPasswordSerializer,
)
from account.tokens import get_tokens_for_user


class RegistrationView(APIView):
    renderer_classes = [AccountRenderer]
    permission_classes = [AllowAny]

    def post(self, request, format=None):
        serializer = AccountSerializer(data=request.data)
        if serializer.is_valid(raise_exception=True):
            user = serializer.save()
            tokens = get_tokens_for_user(user)
            return Response(
                {"message": "Registration Success", "tokens": tokens},
                status=status.HTTP_201_CREATED,
            )
        return Response(
            {"errors": serializer.errors}, status=status.HTTP_400_BAD_REQUEST
        )


class AccountLoginView(APIView):
    permission_classes = [AllowAny]

    def post(self, request, format=None):
        serializer = AccountLoginSerializer(data=request.data)
        if serializer.is_valid(raise_exception=True):
            email = serializer.data.get("email")
            password = serializer.data.get("password")
            user = authenticate(email=email, password=password)
            if user:
                tokens = get_tokens_for_user(user)
                return Response(
                    {"message": "Login Success", "tokens": tokens},
                    status=status.HTTP_200_OK,
                )
            return Response(
                {"errors": {"non_field_errors": ["email or password is invalid"]}},
                status=status.HTTP_404_NOT_FOUND,
            )
        return Response(
            {"errors": serializer.errors}, status=status.HTTP_400_BAD_REQUEST
        )


class AccountProfileView(APIView):
    renderer_classes = [AccountRenderer]
    permission_classes = [IsAuthenticated]

    def get(self, request, format=None):
        serializer = AccountProfileSerializer(request.user)
        return Response(serializer.data, status=status.HTTP_200_OK)


class AccountChangePasswordView(APIView):
    renderer_classes = [AccountRenderer]
    permission_classes = [IsAuthenticated]

    def post(self, request, format=None):
        user = request.user
        serializer = AccountChangePasswordSerializer(data=request.data)
        if serializer.is_valid(raise_exception=True):
            user.set_password(request.data.get("password"))
            user.save()
            return Response(
                {"message": "Password changed successfully"}, status=status.HTTP_200_OK
            )
        return Response(
            {"errors": serializer.errors}, status=status.HTTP_400_BAD_REQUEST
        )


class AccountResetPasswordEmailView(APIView):
    renderer_classes = [AccountRenderer]
    permission_classes = [AllowAny]

    def post(self, request, format=None):
        serializer = AccountResetPasswordEmailSerializer(data=request.data)
        if serializer.is_valid(raise_exception=True):
            return Response(
                {"message": "Password reset email sent successfully"},
                status=status.HTTP_200_OK,
            )
        return Response(
            {"errors": serializer.errors}, status=status.HTTP_400_BAD_REQUEST
        )


class AccountResetPasswordView(APIView):
    renderer_classes = [AccountRenderer]
    permission_classes = [AllowAny]

    def post(self, request, uid, token, format=None):
        serializer = AccountResetPasswordSerializer(
            data=request.data, context={"uid": uid, "token": token}
        )
        if serializer.is_valid(raise_exception=True):
            return Response(
                {"message": "Password reset successfully"}, status=status.HTTP_200_OK
            )
        return Response(
            {"errors": serializer.errors}, status=status.HTTP_400_BAD_REQUEST
        )
