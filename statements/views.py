from django.views.generic import ListView, DetailView

from . import models


class StatementListView(ListView):
    model = models.Statement


class StatementDetailView(DetailView):
    model = models.Statement


class PersonDetailView(DetailView):
    model = models.Person