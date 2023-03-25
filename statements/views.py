from django.db.models import Count, Q, F
from django.shortcuts import get_object_or_404
from django.utils.translation import gettext_lazy as _
from django.views.generic import ListView, DetailView

from . import models


class StatementListView(ListView):
    title = _("All Statements")
    is_home = True

    def get_queryset(self):
        return models.Statement.objects.reviewed().order_by("-created_at")

    def total(self):
        return models.Statement.objects.reviewed().count()

    def people(self):
        return models.Person.objects.annotate(
            items=Count("statements__id", filter=Q(statements__review__isnull=False)),
        ).filter(items__gte=1)

    def topics(self):
        return models.Topic.objects.annotate(
            items=Count("statements__id", filter=Q(statements__review__isnull=False)),
        ).filter(items__gte=1)

    def get_statements(self):
        return models.Statement.objects.reviewed()[:5]


class PersonDetailView(StatementListView):
    is_home = False

    def get(self, request, *args, **kwargs):
        self.person = get_object_or_404(models.Person, pk=self.kwargs["pk"])
        return super().get(request, *args, **kwargs)

    def get_queryset(self):
        return super().get_queryset().filter(person=self.person)

    def title(self):
        return self.person.name


class TopicDetailView(StatementListView):
    is_home = False

    def get(self, request, *args, **kwargs):
        self.topic = get_object_or_404(models.Topic, pk=self.kwargs["pk"])
        return super().get(request, *args, **kwargs)

    def title(self):
        return self.topic

    def get_queryset(self):
        return super().get_queryset().filter(topics=self.topic)


class StatementDetailView(DetailView):
    model = models.Statement

    def get_statements(self):
        return models.Statement.objects.reviewed()
