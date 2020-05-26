from django.urls import path

from core.views import VisitedDomains
from core.views import VisitedLinks


urlpatterns = [
    path('visited_links/', VisitedLinks.as_view(), name='visited_links'),
    path('visited_domains/', VisitedDomains.as_view(), name='visited_domains')

]
