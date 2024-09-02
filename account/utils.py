import os

from django.core.mail import EmailMessage


class Util:
    @staticmethod
    def send_email(data):
        email = EmailMessage(
            subject=data["email"]
        )