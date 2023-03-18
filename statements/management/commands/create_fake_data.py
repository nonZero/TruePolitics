import json
import random

import tqdm
from django.conf import settings
from django.core.management.base import BaseCommand
from faker import Faker

from statements.models import Person, Topic, Statement, Resource

TOPICS = """
מדיני
בטחוני
כלכלי
משפטי
חינוך
חרדים
""".strip().splitlines()


class Command(BaseCommand):
    help = "Create fake data"

    def add_arguments(self, parser):
        parser.add_argument("n", type=int)

    def handle(self, n, *args, **options):
        # Resource.objects.all().delete()
        # Statement.objects.all().delete()
        # Topic.objects.all().delete()
        # Person.objects.all().delete()

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

        for i in tqdm.tqdm(range(n)):
            #
            rating = None if random.randint(1, 4) > 1 else random.randint(1, 3)
            d = faker.date_this_year()
            s = Statement.objects.create(
                person=Person.objects.order_by("?").first(),
                content=faker.paragraph(),
                rating=rating,
                review="\n".join(faker.paragraphs(random.randint(1, 3)))
                if rating
                else None,
                date=d,
                review_date=d,
            )
            s.topics.set(
                list(Topic.objects.order_by("?")[: random.randint(10, 22) // 10]),
            )
            r = s.resources.create(
                type=Resource.ResourceType.OTHER,
                url=faker.url() + f"?x={random.randint(100000, 999999)}",
                content=faker.paragraph(),
                timestamp=f"{d} {faker.time()}+0000",
            )
