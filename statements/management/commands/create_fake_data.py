import random

import tqdm
from django.core.management.base import BaseCommand
from faker import Faker

from statements.models import Person, Topic, Statement, Resource, ResourceStatement


class Command(BaseCommand):
    help = "Create fake data"

    def add_arguments(self, parser):
        parser.add_argument("n", type=int)

    def handle(self, n, *args, **options):
        faker = Faker()
        for i in range(20):
            Person.objects.create(
                name=faker.name(),
                affiliation=faker.company(),
            )

        for i in range(10):
            Topic.objects.create(
                title=faker.color().title(),
            )

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
            )
            s.topics.set(
                list(Topic.objects.order_by("?")[: random.randint(10, 22) // 10]),
            )

            r = Resource.objects.create(
                url=faker.url(),
                content=faker.paragraph(),
                timestamp=d,
            )
            ResourceStatement.objects.create(
                resource=r,
                statement=s,
                priority=1,
            )
