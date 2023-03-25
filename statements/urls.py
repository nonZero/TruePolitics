from django.urls import path

from statements import views

app_name = "s"

urlpatterns = [
    path("", views.StatementListView.as_view(), name="list"),
    path("p/<int:pk>/", views.PersonDetailView.as_view(), name="person"),
    path("t/<int:pk>/", views.TopicDetailView.as_view(), name="topic"),
    path("s/<int:pk>/", views.StatementDetailView.as_view(), name="detail"),
]
