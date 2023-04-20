from rest_framework import serializers

from . import models


class PersonSerializer(serializers.ModelSerializer):
    class Meta:
        model = models.Person
        fields = (
            "id",
            "name",
            "title",
            "affiliation",
            "img_url",
        )


class TopicSerializer(serializers.ModelSerializer):
    class Meta:
        model = models.Topic
        fields = (
            "id",
            "title",
            "description",
        )


class StatementTypeSerializer(serializers.Serializer):
    def to_representation(self, instance: int):
        t = models.Statement.StatementType(instance)
        return {
            "id": t,
            "key": t.name,
            "text": t.label,
        }


class StatementSerializer(serializers.ModelSerializer):
    person = PersonSerializer()
    topics = TopicSerializer(many=True)
    type = StatementTypeSerializer(read_only=True)

    class Meta:
        model = models.Statement
        fields = (
            "id",
            "person",
            "type",
            "content",
            "reviewed_by",
            "review",
            "review_url",
            "review_date",
            "topics",
            "img_url",
        )
