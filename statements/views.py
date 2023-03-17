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
