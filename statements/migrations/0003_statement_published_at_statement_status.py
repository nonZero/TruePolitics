# Generated by Django 4.1.7 on 2023-03-28 13:55

from django.db import migrations, models
from django.utils import timezone


class Migration(migrations.Migration):
    dependencies = [
        ("statements", "0002_alter_statement_url"),
    ]

    operations = [
        migrations.AddField(
            model_name="statement",
            name="published_at",
            field=models.DateTimeField(
                blank=True, null=True, verbose_name="published at", default=timezone.now
            ),
            preserve_default=False,
        ),
        migrations.AddField(
            model_name="statement",
            name="status",
            field=models.IntegerField(
                choices=[(1, "Draft"), (10, "Published"), (200, "Deleted")],
                default=10,
                verbose_name="publish status",
            ),
        ),
    ]
