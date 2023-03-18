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
        return models.Person.objects.filter(statements__isnull=False).annotate(
            items=Count("statements__id", filter=Q(statements__review__isnull=False)),
        )[:8]

    def topics(self):
        return models.Topic.objects.annotate(
            items=Count("statements__id", filter=Q(statements__review__isnull=False)),
        )[:8]

    def get_statements(self):
        return models.Statement.objects.reviewed()[:5]


class StatementDetailView(DetailView):
    model = models.Statement

    def get_statements(self):
        return models.Statement.objects.reviewed()


class PersonDetailView(DetailView):
    model = models.Person

    def title(self):
        return self.object.name

    def get_topics(self):
        n = self.object.statements.reviewed().count()
        return (
            models.Topic.objects.filter(
                statements__review__isnull=False, statements__person=self.object
            )
            .annotate(
                items=Count("statements__id"),
            )
            .distinct()
            .annotate(
                percent=(F("items") * 100 / (n)),
            )
        )

    def get_statements(self):
        return self.object.statements.reviewed()

    def get_statements_count(self):
        return self.get_statements().count()


class PersonTopicDetailView(PersonDetailView):
    def get_statements(self):
        return super().get_statements().filter(topics=self.topic)

    def get(self, request, *args, **kwargs):
        self.topic = get_object_or_404(models.Topic, pk=self.kwargs["topic_pk"])

        return super().get(request, *args, **kwargs)


class TopicDetailView(DetailView):
    model = models.Topic

    def title(self):
        return self.object

    def get_statements(self):
        return models.Statement.objects.reviewed().filter(topics=self.object)

    def get_people(self):
        n = self.object.statements.reviewed().count()
        return (
            models.Person.objects.filter(
                statements__topics=self.object, statements__review__isnull=False
            )
            .annotate(
                items=Count("statements__id"),
            )
            .distinct()
            .annotate(
                percent=(F("items") * 100 / (n)),
            )
        )


class TopicPersonDetailView(TopicDetailView):
    def get_statements(self):
        return super().get_statements().filter(person=self.person)

    def get(self, request, *args, **kwargs):
        self.person = get_object_or_404(models.Person, pk=self.kwargs["person_pk"])

        return super().get(request, *args, **kwargs)
