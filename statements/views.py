from django.views.generic import ListView, DetailView

from . import models


class StatementListView(ListView):
    model = models.Statement
    paginate_by = 20


class StatementDetailView(DetailView):
    model = models.Statement


class PersonDetailView(DetailView):
    model = models.Person
    def get_topics(self):
        return models.Topic.objects.filter(statements__person=self.object).distinct()