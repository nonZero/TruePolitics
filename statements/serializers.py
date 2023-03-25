from rest_framework.serializers import ModelSerializer

from . import models


class PersonSerializer(ModelSerializer):
    class Meta:
        model = models.Person
        fields = (
            "id",
            "name",
            "title",
            "affiliation",
            "img_url",
        )


class TopicSerializer(ModelSerializer):
    class Meta:
        model = models.Topic
        fields = (
            "id",
            "title",
            "description",
        )


class StatementSerializer(ModelSerializer):
    person = PersonSerializer()
    topics = TopicSerializer(many=True)

    class Meta:
        model = models.Statement
        fields = (
            "id",
            "person",
            "content",
            "reviewed_by",
            "review",
            "review_url",
            "review_date",
            "topics",
            "img_url",
        )
