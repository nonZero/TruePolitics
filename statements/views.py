from django.shortcuts import get_object_or_404
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
        return self.object.statements.all()


class PersonTopicDetailView(PersonDetailView):
    def get_statements(self):
        return super().get_statements().filter(topics=self.topic)

    def get(self, request, *args, **kwargs):
        self.topic = get_object_or_404(models.Topic, pk=self.kwargs["topic_pk"])

        return super().get(request, *args, **kwargs)
