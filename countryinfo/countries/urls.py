from django.urls import path
from .views import *

country_list = CountryViewSet.as_view({
    'get': 'list',
    'post': 'create',
})

country_detail = CountryViewSet.as_view({
    'get': 'retrieve',
    'put': 'update',
    'patch': 'partial_update',
    'delete': 'destroy',
})

country_same_region = CountryViewSet.as_view({
    'get': 'same_region',
})

country_by_language = CountryViewSet.as_view({
    'get': 'by_language',
})


urlpatterns = [
    path('', country_list_view, name=''),
    path('countries/', country_list, name='country-list'),
    path('countries/<int:pk>/', country_detail, name='country_detail'),
    path('countries/<int:pk>/same_region/', country_same_region, name='country-same-region'),
    path('countries/by_language/', country_by_language, name='country-by-language'),


]
