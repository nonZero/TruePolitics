import json

import tqdm
from django.conf import settings
from django.core.management.base import BaseCommand

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
תרבות
""".strip().splitlines()


class Command(BaseCommand):
    help = "Create fake data"

    def handle(self, *args, **options):
        mks = json.load((settings.BASE_DIR / "statements" / "data" / "mks.json").open())
        for p in tqdm.tqdm(mks):
            Person.objects.update_or_create(
                name=p["name"],
                defaults=dict(
                    affiliation=p["party"].strip(),
                    img_url=p["img_url"].strip(),
                ),
            )

        gov = json.load((settings.BASE_DIR / "statements" / "data" / "gov.json").open())
        for p in tqdm.tqdm(gov):
            d = dict(
                title=p["PositionName"].strip(),
            )
            if a := p.get("FactionName"):
                d["affiliation"] = a.strip()
            Person.objects.update_or_create(
                name=p["MkName"].strip(),
                defaults=d,
            )

        for t in TOPICS:
            Topic.objects.get_or_create(title=t)
