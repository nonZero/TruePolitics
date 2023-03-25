from django.conf import settings
from django.contrib.auth import get_user_model
from django.core.management.base import BaseCommand
from django.db import IntegrityError


User = get_user_model()


class Command(BaseCommand):
    help = "Create debug users."

    def handle(self, *args, **options):
        assert settings.DEBUG
        try:
            print(User.objects.create_superuser("sysop", password="sysop"))
        except IntegrityError:
            print("exists")
