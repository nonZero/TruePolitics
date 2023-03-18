# Generated by Django 4.1.7 on 2023-03-18 07:45

from django.db import migrations, models
import django.utils.timezone


class Migration(migrations.Migration):
    dependencies = [
        ("statements", "0002_statement_review_date"),
    ]

    operations = [
        migrations.AddField(
            model_name="statement",
            name="created_at",
            field=models.DateTimeField(
                auto_now_add=True, default=django.utils.timezone.now
            ),
            preserve_default=False,
        ),
        migrations.AddField(
            model_name="statement",
            name="updated_at",
            field=models.DateTimeField(auto_now=True),
        ),
        migrations.AlterField(
            model_name="statement",
            name="review_date",
            field=models.DateField(
                default=django.utils.timezone.now, verbose_name="review_date"
            ),
            preserve_default=False,
        ),
    ]
