import json

import tqdm
from django.conf import settings
from django.core.management.base import BaseCommand
from faker import Faker

from statements.models import Person, Topic

TOPICS = """
מדיני
בטחוני
כלכלי
משפטי
חינוך
חרדים
דת
דיור
פוליטי
פנים
תחבורה
""".strip().splitlines()


class Command(BaseCommand):
    help = "Create fake data"

    def handle(self, *args, **options):
        mks = json.load((settings.BASE_DIR / "statements" / "data" / "mks.json").open())

        faker = Faker("he")
        for mk in tqdm.tqdm(mks):
            Person.objects.update_or_create(
                name=mk["name"],
                defaults=dict(
                    affiliation=mk["party"],
                    img_url=mk["img_url"],
                ),
            )

        for t in TOPICS:
            Topic.objects.get_or_create(title=t)
