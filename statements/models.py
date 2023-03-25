from django.db import models
from django.db.models import Count, Q
from django.urls import reverse
from django.utils.translation import gettext_lazy as _


class PersonQuerySet(models.QuerySet):
    def with_reviewed_counts(self):
        return self.annotate(
            items=Count("statements__id", filter=Q(statements__review__isnull=False)),
        ).filter(items__gte=1)


class Person(models.Model):
    name = models.CharField(_("name"), max_length=250, unique=True)
    affiliation = models.CharField(_("affiliation"), max_length=500, blank=False)
    title = models.CharField(_("title"), max_length=200, blank=True, null=True)
    img_url = models.URLField(_("image url"), max_length=3000, null=True)

    objects = PersonQuerySet.as_manager()

    def __str__(self):
        return self.name

    def get_absolute_url(self):
        return reverse("s:person", kwargs={"pk": self.pk})

    class Meta:
        verbose_name = _("person")
        verbose_name_plural = _("people")

    def rating(self):
        return (
            self.statements.filter(rating__isnull=False)
            .aggregate(r=models.Avg("rating"))
            .get("r")
        )


class TopicQuerySet(models.QuerySet):
    def with_reviewed_counts(self):
        return self.annotate(
            items=Count("statements__id", filter=Q(statements__review__isnull=False)),
        ).filter(items__gte=1)


class Topic(models.Model):
    title = models.CharField(_("title"), max_length=250, unique=True)
    description = models.TextField(_("description"), blank=True)

    objects = TopicQuerySet.as_manager()

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

    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    person = models.ForeignKey(
        Person, models.PROTECT, related_name="statements", verbose_name=_("person")
    )
    content = models.TextField(_("statement content"))
    date = models.DateField(_("date said"))
    url = models.URLField(_("statement url"), null=True, blank=True)

    reviewed_by = models.CharField(
        _("reviewed by"), max_length=200, blank=True, null=True
    )
    review = models.TextField(blank=True, null=True, verbose_name=_("review summary"))
    review_url = models.URLField(_("review url"), max_length=3000, null=True)
    review_date = models.DateField(_("review date"), null=True, blank=True)
    img_url = models.URLField(
        max_length=3000,
        verbose_name=_("image url"),
        blank=True,
        null=True,
    )

    topics = models.ManyToManyField(
        Topic, blank=True, related_name="statements", verbose_name=_("topics")
    )

    rating = models.IntegerField(
        choices=Rating.choices,
        null=True,
        verbose_name=_("rating"),
        blank=True,
    )

    detailed_content = models.TextField(
        _("detailed content"),
        help_text=_("detailed article about this item"),
        blank=True,
        null=True,
    )

    objects = StatementQuerySet.as_manager()

    class Meta:
        verbose_name = _("statement")
        verbose_name_plural = _("statements")

    def __str__(self):
        return f'"{self.content}" by {self.person}'
