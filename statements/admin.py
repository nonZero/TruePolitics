from django.contrib import admin
from django.db.models import Q, ManyToManyField
from django.forms import CheckboxSelectMultiple
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
    radio_fields = {
        "status": admin.VERTICAL,
        "type": admin.HORIZONTAL,
    }
    formfield_overrides = {
        ManyToManyField: {"widget": CheckboxSelectMultiple},
    }

    def get_topics(self, instance):
        return ", ".join(str(t) for t in instance.topics.all())

    get_topics.short_description = _("topics")


class PublishedItemsFilter(admin.SimpleListFilter):
    title = _("published items")
    parameter_name = "with_items"

    def lookups(self, request, model_admin):
        return (
            ("with", _("have published items")),
            ("without", _("does not have published items")),
        )

    def queryset(self, request, queryset):
        if v := self.value():
            return queryset.filter(Q(items__gt=0) if v == "with" else Q(items=0))


@admin.register(models.Person)
class PersonAdmin(admin.ModelAdmin):
    def get_queryset(self, request):
        return super().get_queryset(request)._with_reviewed_counts()

    ordering = ("name",)

    list_per_page = 250
    list_max_show_all = 1000
    list_display = (
        "name",
        "affiliation",
        "title",
        "items",
        "has_image",
    )
    list_filter = (
        PublishedItemsFilter,
        "affiliation",
    )
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
