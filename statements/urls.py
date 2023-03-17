from django.urls import path

from statements import views

app_name = "s"

urlpatterns = [
    path("", views.StatementListView.as_view(), name="list"),
    path("<int:pk>/", views.StatementDetailView.as_view(), name="detail"),
]
