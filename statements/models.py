from django.db import models
from django.utils.translation import gettext_lazy as _


class Person(models.Model):
    name = models.CharField(_("name"), max_length=250, unique=True)
    affiliation = models.CharField(_("affiliation"), max_length=500, blank=False)
    title = models.CharField(_("title"), max_length=200, blank=True, null=True)
    img_url = models.URLField(_("image url"), null=True)

    def __str__(self):
        return self.name

    class Meta:
        verbose_name = _("person")
        verbose_name_plural = _("people")


class Topic(models.Model):
    title = models.CharField(_("title"), max_length=250, unique=True)
    description = models.TextField(_("description"), blank=True)

    def __str__(self):
        return self.title

    class Meta:
        verbose_name = _("topic")
        verbose_name_plural = _("topics")


class Statement(models.Model):
    person = models.ForeignKey(
        Person, models.PROTECT, related_name="statements", verbose_name=_("person")
    )
    topics = models.ManyToManyField(
        Topic, blank=True, related_name="statements", verbose_name=_("topics")
    )
    date = models.DateField(_("date"))
    content = models.TextField(_("content"))

    class Meta:
        verbose_name = _("statement")
        verbose_name_plural = _("statements")

    def __str__(self):
        return f'"{self.content}" by {self.person}'

    class Rating(models.IntegerChoices):
        GREEN = 1, _("True")
        ORANGE = 2, _("Half True")
        RED = 3, _("False")

    rating = models.IntegerField(
        choices=Rating.choices, null=True, verbose_name=_("rating")
    )
    review = models.TextField(blank=True, null=True, verbose_name=_("review"))


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
