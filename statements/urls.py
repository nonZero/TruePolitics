from django.urls import path

from statements import views

app_name = "s"

urlpatterns = [
    path("", views.StatementListView.as_view(), name="list"),
    path("s/<int:pk>/", views.StatementDetailView.as_view(), name="detail"),
    path("p/<int:pk>/", views.PersonDetailView.as_view(), name="person"),
    path(
        "p/<int:pk>/<int:topic_pk>/",
        views.PersonTopicDetailView.as_view(),
        name="person_topic",
    ),
    path("t/<int:pk>/", views.TopicDetailView.as_view(), name="topic"),
    path(
        "t/<int:pk>/<int:person_pk>/",
        views.TopicPersonDetailView.as_view(),
        name="topic_person",
    ),
]
