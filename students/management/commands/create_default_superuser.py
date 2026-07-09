
from django.core.management.base import BaseCommand
from django.contrib.auth.models import User
from decouple import config


class Command(BaseCommand):
    help = "Creates a default superuser if it does not exist."

    def handle(self, *args, **kwargs):

        username = config("ADMIN_USERNAME")
        email = config("ADMIN_EMAIL")
        password = config("ADMIN_PASSWORD")

        if User.objects.filter(username=username).exists():
            self.stdout.write(
                self.style.WARNING(
                    f'Superuser "{username}" already exists.'
                )
            )
            return

        User.objects.create_superuser(
            username=username,
            email=email,
            password=password
        )

        self.stdout.write(
            self.style.SUCCESS(
                f'Superuser "{username}" created successfully.'
            )
        )