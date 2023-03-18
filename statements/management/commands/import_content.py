import json
import random
from pprint import pp

import pandas as pd
import tqdm
from django.conf import settings
from django.core.management.base import BaseCommand
from faker import Faker

from statements.models import Person, Topic, Statement, Resource

REVIEWERS = """
בן כספית
גיא זוהר
""".strip().splitlines()


COLS = """
topic,נושא
person,פוליטיקאי
content,טענה
date,תאריך
resource_url,מקור טענה
type,הבטחה
review,הפרכה
review_date,תאריך הפרכה
review_url,מקור הפרכה
""".strip().splitlines()

COLS = dict(s.split(",")[::-1] for s in COLS)


class Command(BaseCommand):
    help = "import content"

    def handle(self, *args, **options):
        df = pd.read_csv(
            settings.BASE_DIR / "statements/data/content.csv", dtype=str
        ).rename(
            columns=COLS,
        )
        df = df.apply(lambda s: s.str.strip())
        df = df.mask(pd.isna(df), None)
        # assert set(df.columns) == set(COLS.keys())

        # print(df.to_csv(index=False))

        # df = df[df.review != ""]
        # df = df.iloc[:16]

        Resource.objects.all().delete()
        Statement.objects.all().delete()

        faker = Faker("he")

        for row in tqdm.tqdm(df.itertuples()):
            try:
                #
                print(row.person)
                p = Person.objects.get(name=row.person)
                s = Statement.objects.create(
                    person=p,
                    content=row.content,
                    rating=Statement.Rating.RED,
                    review=row.review,
                    review_url=row.review_url,
                    date=row.date or None,
                    review_date=row.review_date or None,
                    reviewed_by=random.choice(REVIEWERS),
                    img_url=faker.image_url(400, 300),
                )
                print(row.topic.strip())
                s.topics.add(Topic.objects.get(title=row.topic.strip()))
                if "twitter" in row.resource_url:
                    rt = Resource.ResourceType.TWEET
                else:
                    rt = Resource.ResourceType.OTHER

                s.resources.create(
                    type=rt,
                    url=row.resource_url,
                    # content=faker.paragraph(),
                    timestamp=row.date,
                )
            except Exception as e:
                print(row)
                print(e)
                # raise
