from django.contrib.auth.tokens import PasswordResetTokenGenerator
from django.core.mail import send_mail
from django.utils.encoding import smart_str, force_bytes, DjangoUnicodeDecodeError
from django.utils.http import urlsafe_base64_decode, urlsafe_base64_encode
from rest_framework import serializers

from account.models import Account


class AccountSerializer(serializers.ModelSerializer):
    password2 = serializers.CharField(style={"input_type": "password"}, write_only=True)

    class Meta:
        model = Account
        fields = [
            "email",
            "name",
            "password",
            "password2",
            "terms",
            "date_of_birth",
            "is_active",
            "is_admin",
            "created",
            "updated",
        ]
        extra_kwargs = {"password": {"write_only": True}}

    def validate(self, attrs):
        password = attrs.get("password")
        password2 = attrs.get("password2")
        if password != password2:
            raise serializers.ValidationError("Passwords does not match")
        return attrs

    def create(self, validated_data):
        return Account.objects.create_user(**validated_data)


class AccountLoginSerializer(serializers.ModelSerializer):
    email = serializers.EmailField(max_length=255)

    class Meta:
        model = Account
        fields = ["email", "password"]


class AccountProfileSerializer(serializers.ModelSerializer):
    class Meta:
        model = Account
        fields = [
            "id",
            "email",
            "name",
            "terms",
            "date_of_birth",
            "is_active",
            "is_admin",
            "created",
            "updated",
        ]


class AccountChangePasswordSerializer(serializers.Serializer):
    password = serializers.CharField(
        max_length=255, style={"input_type": "password"}, write_only=True
    )
    password2 = serializers.CharField(
        max_length=255, style={"input_type": "password"}, write_only=True
    )

    class Meta:
        fields = ["password", "password2"]

    def validate(self, attrs):
        password = attrs.get("password")
        password2 = attrs.get("password2")
        if password != password2:
            raise serializers.ValidationError("Passwords does not match")
        return attrs


class AccountResetPasswordEmailSerializer(serializers.Serializer):
    email = serializers.EmailField(max_length=255)

    class Meta:
        fields = ["email"]

    def validate(self, attrs):
        email = attrs.get("email")
        try:
            account = Account.objects.get(email=email)
            uid = urlsafe_base64_encode(force_bytes(account.id))
            token = PasswordResetTokenGenerator().make_token(account)
            link = f"http://localhost.3000/account/reset/{uid}/{token}"
            body = f"""Hi {account.name},\nClick the link below to reset your password.\n\n{link}\n\nRegards,\nDjango dev app"""
            send_mail(
                subject="Reset password",
                message=body,
                from_email=None,
                recipient_list=[account.email],
            )
            return attrs
        except Account.DoesNotExist:
            raise serializers.ValidationError("User with given email does not exists")


class AccountResetPasswordSerializer(serializers.Serializer):
    password = serializers.CharField(
        max_length=255, style={"input_type": "password"}, write_only=True
    )
    password2 = serializers.CharField(
        max_length=255, style={"input_type": "password"}, write_only=True
    )

    class Meta:
        fields = ["password", "password2"]

    def validate(self, attrs):
        try:
            password = attrs.get("password")
            password2 = attrs.get("password2")
            uid = self.context.get("uid")
            token = self.context.get("token")
            if password != password2:
                raise serializers.ValidationError("Passwords does not match")
            id = smart_str(urlsafe_base64_decode(uid))
            account = Account.objects.get(id=id)
            if not PasswordResetTokenGenerator().check_token(user=account, token=token):
                raise serializers.ValidationError("Token invalid or expired")
            else:
                account.set_password(password)
                account.save()
                return attrs
        except DjangoUnicodeDecodeError:
            raise serializers.ValidationError("Token invalid or expired")
