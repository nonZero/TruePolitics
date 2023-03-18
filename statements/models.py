from django.db import models
from django.urls import reverse
from django.utils.translation import gettext_lazy as _


class Person(models.Model):
    name = models.CharField(_("name"), max_length=250, unique=True)
    affiliation = models.CharField(_("affiliation"), max_length=500, blank=False)
    title = models.CharField(_("title"), max_length=200, blank=True, null=True)
    img_url = models.URLField(_("image url"), max_length=3000, null=True)

    def __str__(self):
        return self.name

    def get_absolute_url(self):
        return reverse("s:person", kwargs={"pk": self.pk})

    def get_topic_statements_count(self, topic):
        return self.statements.filter(topic=topic, review__isnull=False).count()

    class Meta:
        verbose_name = _("person")
        verbose_name_plural = _("people")

    def rating(self):
        return (
            self.statements.filter(rating__isnull=False)
            .aggregate(r=models.Avg("rating"))
            .get("r")
        )


class Topic(models.Model):
    title = models.CharField(_("title"), max_length=250, unique=True)
    description = models.TextField(_("description"), blank=True)

    class Meta:
        verbose_name = _("topic")
        verbose_name_plural = _("topics")

    def __str__(self):
        return self.title

    def get_absolute_url(self):
        return reverse("s:topic", kwargs={"pk": self.pk})


class StatementQuerySet(models.QuerySet):
    def reviewed(self):
        return self.filter(review__isnull=False)


class Statement(models.Model):
    class Rating(models.IntegerChoices):
        GREEN = 1, _("True")
        ORANGE = 2, _("Half True")
        RED = 3, _("False")

    person = models.ForeignKey(
        Person, models.PROTECT, related_name="statements", verbose_name=_("person")
    )
    topics = models.ManyToManyField(
        Topic, blank=True, related_name="statements", verbose_name=_("topics")
    )
    date = models.DateField(_("date"))
    content = models.TextField(_("content"))
    rating = models.IntegerField(
        choices=Rating.choices,
        null=True,
        verbose_name=_("rating"),
        blank=True,
    )
    review = models.TextField(blank=True, null=True, verbose_name=_("review"))
    review_date = models.DateField(_("review_date"))
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    reviewed_by = models.CharField(
        _("reviewed_by"), max_length=200, blank=True, null=True
    )
    img_url = models.URLField(null=True, max_length=3000)
    objects = StatementQuerySet.as_manager()

    class Meta:
        verbose_name = _("statement")
        verbose_name_plural = _("statements")

    def __str__(self):
        return f'"{self.content}" by {self.person}'


class Resource(models.Model):
    class ResourceType(models.IntegerChoices):
        OTHER = 1, _("Other")
        TWEET = 10, _("Tweet")
        HAARETZ = 11, _("Haaretz")
        YNET = 12, _("YNet")

    # uid = models.CharField(...)
    # type = twit, web arcitle, facebook post
    statement = models.ForeignKey(
        Statement, models.PROTECT, blank=True, related_name="resources"
    )
    url = models.URLField(max_length=3000)
    timestamp = models.DateTimeField()
    type = models.IntegerField(choices=ResourceType.choices, default=ResourceType.TWEET)
    content = models.TextField()
    note = models.TextField(blank=True)

    class Meta:
        unique_together = (
            "statement",
            "url",
        )

    def __str__(self):
        return self.content
