from django.urls import path, include
from pravesh.views import dashboard, upload_document

urlpatterns = [
    path("accounts/",include("django.contrib.auth.urls")),
    path('dashboard/',dashboard, name="dashboard"),
    path('upload/',upload_document, name="upload"),
    path('',dashboard),

    ]