from django.db.models import Count, Q
from django.shortcuts import get_object_or_404
from django.urls import reverse
from django.views.generic import ListView, DetailView
from django.utils.translation import gettext_lazy as _

from . import models


class StatementListView(ListView):
    title = _("Home Page")
    paginate_by = 20

    def get_queryset(self):
        return models.Statement.objects.reviewed()

    def people(self):
        return models.Person.objects.annotate(
            items=Count("statements__id", filter=Q(statements__review__isnull=False)),
        )[:8]

    def topics(self):
        return models.Topic.objects.annotate(
            items=Count("statements__id", filter=Q(statements__review__isnull=False)),
        )[:8]


class StatementDetailView(DetailView):
    model = models.Statement


class PersonDetailView(DetailView):
    model = models.Person

    def title(self):
        return self.object.name

    def get_topics(self):
        return models.Topic.objects.filter(
            statements__person=self.object, statements__review__isnull=False
        ).distinct()

    def get_statements(self):
        return self.object.statements.reviewed()

    def get_statements_count(self):
        return self.get_statements().count()

    def get_topics_names(self):
        return [
            {
                "id": t.id,
                "title": t.title,
                "url": reverse(
                    "s:person_topic", kwargs={"pk": self.object.pk, "topic_pk": t.pk}
                ),
            }
            for t in self.get_topics()
        ]


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
        return models.Person.objects.filter(
            statements__topics=self.object, statements__review__isnull=False
        ).distinct()

    def get_people_names(self):
        return [
            {
                "id": p.id,
                "name": p.name,
                "url": reverse(
                    "s:topic_person", kwargs={"pk": self.object.pk, "person_pk": p.pk}
                ),
            }
            for p in self.get_people()
        ]


class TopicPersonDetailView(TopicDetailView):
    def get_statements(self):
        return super().get_statements().filter(person=self.person)

    def get(self, request, *args, **kwargs):
        self.person = get_object_or_404(models.Person, pk=self.kwargs["person_pk"])

        return super().get(request, *args, **kwargs)
