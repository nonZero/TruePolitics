from django.contrib import admin
from django.utils.translation import gettext_lazy as _

from statements import models

admin.site.register(models.Topic)
admin.site.register(models.Person)


@admin.register(models.Statement)
class StatementAdmin(admin.ModelAdmin):
    list_display = (
        "person",
        "content",
        "date",
        "get_topics",
        "rating",
    )
    list_filter = ("topics",)
    date_hierarchy = "date"
    search_fields = ("content", "person__name")

    def get_topics(self, instance):
        return ", ".join(str(t) for t in instance.topics.all())

    get_topics.short_description = _("topics")
