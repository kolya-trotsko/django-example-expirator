from .views import LoginUser, DomainsView, logout_user
from django.urls import path
from rest_framework.urlpatterns import format_suffix_patterns
from .api import *

urlpatterns = [
    path('', DomainsView.index, name='index'),
    path('about/', DomainsView.about, name='about'),
    path('login/', LoginUser.as_view(), name='login'),
    path('logout/', logout_user, name='logout'),
    path('dns/', DomainsView.dns, name='DNS_Records'),
    path('services/', DomainsView.services, name='services'),
    path('campaigns/', DomainsView.campaigns, name='campaigns'),
    path('api', DomainViewApi.as_view()),
    path('api/login', LoginApi.as_view()),
    path('api/addService', AddService.as_view()),
    path('api/getService', GetService.as_view()),
    path('api/delService', DelService.as_view()),
    path('api/ArchivedDomain', ArchivedDomain.as_view()),
    path('api/unArchivedDomain', unArchivedDomain.as_view()),
    path('api/delDomain', DelDomain.as_view()),
]
urlpatterns = format_suffix_patterns(urlpatterns)