from django.urls import path  # type: ignore

from main.views import VisitedLinksAPIView, VisitedDomainsAPIView

urlpatterns = [
    path('visited_links/', VisitedLinksAPIView.as_view()),
    path('visited_domains/', VisitedDomainsAPIView.as_view()),
]
