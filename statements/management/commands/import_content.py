from pprint import pp

import pandas as pd
from django.conf import settings
from django.core.management.base import BaseCommand
from django.utils import translation

from statements.models import Person, Topic, Statement

COLS = dict(
    [
        ("תחקירן", "reviewed_by"),
        ("נושא", "topic"),
        ("פוליטיקאי", "person"),
        ("אמירה", "content"),
        ("תאריך אמירה", "date"),
        ("מקור אמירה", "url"),
        ("סוג", "type"),
        ("הפרכה", "review"),
        ("תאריך הפרכה", "review_date"),
        ("מקור הפרכה", "review_url"),
    ]
)


class Command(BaseCommand):
    help = "import content"

    def handle(self, *args, **options):
        translation.activate(settings.LANGUAGE_CODE)
        types = {x.label: x for x in Statement.StatementType}

        df = pd.read_csv(settings.BASE_DIR / "statements/data/content.csv", dtype=str)
        assert set(df.columns) == set(COLS.keys()), set(df.columns) ^ set(COLS.keys())

        df = df.rename(
            columns=COLS,
        )
        df = df.apply(lambda s: s.str.strip())
        df = df.mask(pd.isna(df), None)
        assert set(df.columns) == set(COLS.values()), set(df.columns) ^ set(
            COLS.values()
        )

        # print(df.to_csv(index=False))

        # df = df[df.review != ""]
        # df = df.iloc[:16]

        Statement.objects.all().delete()

        rows = list(df.itertuples())

        for row in rows:
            try:
                p = Person.objects.get(name=row.person)
            except Person.DoesNotExist:
                # print(f"missing: {row.person=}")
                print(repr(row.person))
                print(
                    [
                        p.name
                        for p in Person.objects.filter(
                            name__contains=str(row.person[:4])
                        )
                    ],
                )
                print()
                continue

            d = dict(
                person=p,
                content=row.content,
                type=types[row.type],
                review=row.review,
                date=row.date or None,
                url=row.url or None,
                review_url=row.review_url or None,
                review_date=row.review_date or None,
                reviewed_by=row.reviewed_by or None,
            )

            try:
                if row.review_url:
                    s = Statement.objects.update_or_create(
                        review_url=row.review_url,
                        defaults=d,
                    )[0]
                elif row.url:
                    s = Statement.objects.update_or_create(
                        url=row.url,
                        defaults=d,
                    )[0]
                else:
                    print("missing url:")
                    pp(row)
                    continue
                s.save()
                try:
                    s.topics.add(Topic.objects.get(title=row.topic.strip()))
                except Topic.DoesNotExist:
                    print(f"missing topic: {row.topic=}")

            except:
                pp(row)
                pp(d)
                raise
