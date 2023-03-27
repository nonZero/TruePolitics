from django.contrib import admin
from django.utils.translation import gettext_lazy as _

from statements import models

admin.site.register(models.Topic)


@admin.register(models.Statement)
class StatementAdmin(admin.ModelAdmin):
    list_display = (
        "person",
        "content",
        "date",
        "get_topics",
        "type",
    )
    list_filter = ("topics", "person")
    date_hierarchy = "date"
    search_fields = ("content", "person__name")

    def get_topics(self, instance):
        return ", ".join(str(t) for t in instance.topics.all())

    get_topics.short_description = _("topics")


@admin.register(models.Person)
class PersonAdmin(admin.ModelAdmin):
    list_display = (
        "name",
        "affiliation",
        "title",
        "has_image",
    )
    list_filter = ("affiliation",)
    search_fields = (
        "name",
        "affiliation",
        "title",
    )

    def has_image(self, instance: models.Person):
        return bool(instance.img_url)

    has_image.short_description = _("has image")
    has_image.boolean = True
