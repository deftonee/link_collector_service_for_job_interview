from django.urls import path, include  # type: ignore

from rest_framework.schemas import get_schema_view  # type: ignore


urlpatterns = [
    path('', include('main.urls')),
    path('', get_schema_view()),
]
