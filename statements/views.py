from django.shortcuts import get_object_or_404
from django.urls import reverse
from django.views.generic import ListView, DetailView
from django.utils.translation import gettext_lazy as _

from . import models


class StatementListView(ListView):
    title = _("Home Page")
    model = models.Statement
    paginate_by = 20


class StatementDetailView(DetailView):
    model = models.Statement


class PersonDetailView(DetailView):
    model = models.Person

    def title(self):
        return self.object.name

    def get_topics(self):
        return models.Topic.objects.filter(statements__person=self.object).distinct()

    def get_statements(self):
        return self.object.statements.reviewed()


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
        return models.Statement.objects.filter(topics=self.object)

    def get_people(self):
        return models.Person.objects.filter(statements__topics=self.object).distinct()

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
