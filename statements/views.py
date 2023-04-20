from django.conf import settings
from django.http import JsonResponse
from django.shortcuts import get_object_or_404
from django.utils.translation import gettext_lazy as _
from django.views import View
from django.views.generic import ListView, DetailView

from . import models, serializers


class BaseMixin:
    def get_context_data(self, **kwargs):
        return super().get_context_data(
            google_site_verification=settings.GOOGLE_SITE_VERIFICATION,
            **kwargs,
        )

    def total(self):
        return models.Statement.objects.reviewed().count()

    def people(self):
        return models.Person.objects.with_reviewed_counts().order_by("name")

    def topics(self):
        return models.Topic.objects.with_reviewed_counts().order_by("title")


class StatementListView(BaseMixin, ListView):
    title = _("All Statements")
    is_home = True

    def get_queryset(self):
        return models.Statement.objects.reviewed().order_by("-created_at")


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


class StatementDetailView(BaseMixin, DetailView):
    def get_queryset(self):
        return models.Statement.objects.reviewed()

    def title(self):
        return f"{self.object.person.name}: {self.object.content}"


class StatementExportView(BaseMixin, View):
    def get(self, request, *args, **kwargs):
        d = {
            "items": serializers.StatementSerializer(
                models.Statement.objects.reviewed().order_by("-created_at"),
                many=True,
            ).data,
            "people": serializers.PersonSerializer(self.people(), many=True).data,
            "topics": serializers.TopicSerializer(self.topics(), many=True).data,
        }
        return JsonResponse(d, json_dumps_params={"ensure_ascii": False})
