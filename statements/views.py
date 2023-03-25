from django.db.models import Count, Q, F
from django.shortcuts import get_object_or_404
from django.utils.translation import gettext_lazy as _
from django.views.generic import ListView, DetailView

from . import models


class StatementListView(ListView):
    title = _("Home Page")
    paginate_by = 20

    def get_queryset(self):
        return models.Statement.objects.reviewed()

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


class StatementDetailView(DetailView):
    model = models.Statement

    def get_statements(self):
        return models.Statement.objects.reviewed()


class PersonDetailView(StatementListView):
    def get(self, request, *args, **kwargs):
        self.person = get_object_or_404(models.Person, pk=self.kwargs["pk"])
        return super().get(request, *args, **kwargs)

    def get_queryset(self):
        return super().get_queryset().filter(person=self.person)

    def title(self):
        return self.person.name


class TopicDetailView(StatementListView):
    def get(self, request, *args, **kwargs):
        self.topic = get_object_or_404(models.Topic, pk=self.kwargs["pk"])
        return super().get(request, *args, **kwargs)

    def title(self):
        return self.topic

    def get_queryset(self):
        return super().get_queryset().filter(topics=self.topic)


class PersonTopicDetailView(PersonDetailView):
    def get_statements(self):
        return super().get_statements().filter(topics=self.topic)

    def get(self, request, *args, **kwargs):
        self.topic = get_object_or_404(models.Topic, pk=self.kwargs["topic_pk"])

        return super().get(request, *args, **kwargs)


class TopicPersonDetailView(TopicDetailView):
    def get_statements(self):
        return super().get_statements().filter(person=self.person)

    def get(self, request, *args, **kwargs):
        self.person = get_object_or_404(models.Person, pk=self.kwargs["person_pk"])

        return super().get(request, *args, **kwargs)
