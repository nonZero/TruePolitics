# Generated by Django 4.1.7 on 2023-03-25 06:48

from django.db import migrations, models


class Migration(migrations.Migration):
    dependencies = [
        ("statements", "0007_alter_statement_review_date"),
    ]

    operations = [
        migrations.AlterField(
            model_name="statement",
            name="content",
            field=models.TextField(verbose_name="statement content"),
        ),
        migrations.AlterField(
            model_name="statement",
            name="date",
            field=models.DateField(verbose_name="date said"),
        ),
        migrations.AlterField(
            model_name="statement",
            name="img_url",
            field=models.URLField(max_length=3000, null=True, verbose_name="image url"),
        ),
        migrations.AlterField(
            model_name="statement",
            name="review",
            field=models.TextField(
                blank=True, null=True, verbose_name="review summary"
            ),
        ),
        migrations.AlterField(
            model_name="statement",
            name="reviewed_by",
            field=models.CharField(
                blank=True, max_length=200, null=True, verbose_name="reviewed by"
            ),
        ),
    ]
