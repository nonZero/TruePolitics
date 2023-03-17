from django.contrib import admin

from statements import models

admin.site.register(models.Topic)
admin.site.register(models.Person)


@admin.register(models.Statement)
class StatementAdmin(admin.ModelAdmin):
    list_display = (
        "__str__",
        "date",
        "get_topics",
    )
    list_filter = ("topics",)
    date_hierarchy = "date"
    search_fields = ("content", "person__name")

    def get_topics(self, instance):
        return ", ".join(str(t) for t in instance.topics.all())
