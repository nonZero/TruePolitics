from django.contrib import admin
from django.utils.translation import gettext_lazy as _

from statements import models

admin.site.register(models.Topic)


@admin.register(models.Statement)
class StatementAdmin(admin.ModelAdmin):
    list_display = (
        "content",
        "person",
        "status",
        "date",
        "get_topics",
        "type",
    )
    list_filter = ("status", "topics", "person")
    date_hierarchy = "date"
    search_fields = ("content", "person__name")

    def get_topics(self, instance):
        return ", ".join(str(t) for t in instance.topics.all())

    get_topics.short_description = _("topics")


@admin.register(models.Person)
class PersonAdmin(admin.ModelAdmin):
    def get_queryset(self, request):
        return super().get_queryset(request)._with_reviewed_counts().order_by("-items")

    list_per_page = 250
    list_max_show_all = 1000
    list_display = (
        "name",
        "affiliation",
        "title",
        "items",
        "has_image",
    )
    list_filter = ("affiliation",)
    search_fields = (
        "name",
        "affiliation",
        "title",
    )

    def items(self, instance):
        return instance.items

    items.short_description = _("statements")
    items.admin_order_field = "items"

    def has_image(self, instance: models.Person):
        return bool(instance.img_url)

    has_image.short_description = _("has image")
    has_image.boolean = True

    def has_image(self, instance: models.Person):
        return bool(instance.img_url)

    has_image.short_description = _("has image")
    has_image.boolean = True
