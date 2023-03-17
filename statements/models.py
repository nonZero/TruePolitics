from django.db import models
from django.utils.translation import gettext_lazy as _


class Person(models.Model):
    name = models.CharField(max_length=250, unique=True)
    affiliation = models.CharField(max_length=500, blank=False)

    def __str__(self):
        return self.name

    class Meta:
        verbose_name_plural = _("people")


class Topic(models.Model):
    title = models.CharField(max_length=250, unique=True)
    description = models.TextField(blank=True)

    def __str__(self):
        return self.title

    class Meta:
        verbose_name = _("topic")
        verbose_name_plural = _("topics")


class Statement(models.Model):
    person = models.ForeignKey(Person, models.PROTECT, related_name="statements")
    topics = models.ManyToManyField(Topic, blank=True, related_name="statements")
    date = models.DateField()
    content = models.TextField()

    def __str__(self):
        return f'"{self.content}" by {self.person}'

    class Rating(models.IntegerChoices):
        GREEN = 1, _("True")
        ORANGE = 2, _("Half True")
        RED = 3, _("False")

    rating = models.IntegerField(choices=Rating.choices, null=True)
    review = models.TextField(blank=True, null=True)


class Resource(models.Model):
    # uid = models.CharField(...)
    # type = twit, web arcitle, facebook post
    url = models.URLField(unique=True)
    content = models.TextField()
    timestamp = models.DateTimeField()
    # full_content = models.JSONField()


class ResourceStatement(models.Model):
    statement = models.ForeignKey(Statement, models.PROTECT, related_name="resources")
    resource = models.ForeignKey(Resource, models.PROTECT, related_name="resources")
    priority = models.IntegerField(default=10)
    note = models.TextField(blank=True)
